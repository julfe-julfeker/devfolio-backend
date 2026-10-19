
from django.db import transaction
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

from rest_framework import status, generics, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework.exceptions import ValidationError

from accounts.permissions import IsOwner
from blog.models import Post
from projects.models import Project
from portfolio.models import Skill, Experience
from .models import Comment, ContactMessage, PostLike
from .serializers import CommentSerializer, ContactMessageSerializer


class CommentRateThrottle(AnonRateThrottle):
    scope = "comments"


class ContactRateThrottle(AnonRateThrottle):
    scope = "contact"


class LikeRateThrottle(AnonRateThrottle):
    scope = "likes"



class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        queryset = Comment.objects.filter(
            is_approved=True,
            parent__isnull=True,
            post__status="PUBLISHED",
        ).select_related("post").prefetch_related("replies")

        post_slug = self.request.query_params.get("post")

        if post_slug:
            queryset = queryset.filter(post__slug=post_slug)

        return queryset.order_by("-created_at")

    def get_throttles(self):
        if self.request.method == "POST":
            return [CommentRateThrottle()]
        return []

    def get_serializer_class(self):
        return CommentSerializer

    def perform_create(self, serializer):
        post = serializer.validated_data["post"]

        if post.status != "PUBLISHED":
            raise ValidationError({
                "post": "Comments are allowed only on published posts."
            })

        serializer.save(is_approved=False)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        for comment in response.data:
            comment.pop("email", None)

        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data.pop("email", None)
        return response


class CommentModerationView(APIView):
    permission_classes = [IsOwner]

    def patch(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response(
                {"detail": "Comment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        approved = request.data.get("is_approved")

        if not isinstance(approved, bool):
            return Response(
                {"is_approved": ["Provide true or false."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comment.is_approved = approved
        comment.save(update_fields=["is_approved", "updated_at"])

        return Response({
            "id": comment.id,
            "is_approved": comment.is_approved,
        })

    def delete(self, request, pk):
        deleted, _ = Comment.objects.filter(pk=pk).delete()

        if not deleted:
            return Response(
                {"detail": "Comment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentInboxView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwner]
    queryset = Comment.objects.all().order_by("-created_at")


class ContactCreateView(generics.CreateAPIView):
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactRateThrottle]


class ContactInboxView(generics.ListAPIView):
    serializer_class = ContactMessageSerializer
    permission_classes = [IsOwner]
    queryset = ContactMessage.objects.all().order_by("-created_at")


class ContactDetailView(APIView):
    permission_classes = [IsOwner]

    def patch(self, request, pk):
        try:
            message = ContactMessage.objects.get(pk=pk)
        except ContactMessage.DoesNotExist:
            return Response(
                {"detail": "Message not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_read = request.data.get("is_read")

        if not isinstance(is_read, bool):
            return Response(
                {"is_read": ["Provide true or false."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message.is_read = is_read
        message.save(update_fields=["is_read", "updated_at"])

        return Response({
            "id": message.id,
            "is_read": message.is_read,
        })

    def delete(self, request, pk):
        deleted, _ = ContactMessage.objects.filter(pk=pk).delete()

        if not deleted:
            return Response(
                {"detail": "Message not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeToggleView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LikeRateThrottle]

    def post(self, request, slug):
        visitor_id = request.headers.get("X-Visitor-Id", "").strip()

        if not visitor_id:
            return Response(
                {"detail": "X-Visitor-Id header is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(visitor_id) > 100:
            return Response(
                {"detail": "Invalid visitor ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            post = Post.objects.get(slug=slug, status="PUBLISHED")
        except Post.DoesNotExist:
            return Response(
                {"detail": "Post not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        with transaction.atomic():
            like, created = PostLike.objects.get_or_create(
                post=post,
                visitor_id=visitor_id,
            )

            if not created:
                like.delete()

        return Response({
            "liked": created,
            "likes_count": PostLike.objects.filter(post=post).count(),
        })


class DashboardStatsView(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        return Response({
            "total_posts": Post.objects.count(),
            "published_posts": Post.objects.filter(
                status="PUBLISHED"
            ).count(),
            "draft_posts": Post.objects.filter(
                status="DRAFT"
            ).count(),
            "total_projects": Project.objects.count(),
            "total_skills": Skill.objects.count(),
            "total_experiences": Experience.objects.count(),
            "total_comments": Comment.objects.count(),
            "pending_comments": Comment.objects.filter(
                is_approved=False
            ).count(),
            "total_messages": ContactMessage.objects.count(),
            "unread_messages": ContactMessage.objects.filter(
                is_read=False
            ).count(),
            "total_likes": PostLike.objects.count(),
            "total_views": sum(
                Post.objects.values_list("views_count", flat=True)
            ),
        })
