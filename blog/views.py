
from django.db.models import Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from accounts.permissions import IsOwnerOrReadOnly
from .models import Category, Tag, Post
from .serializers import (
    CategorySerializer, TagSerializer, PostSerializer
)


class PostPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "slug"

    def get_queryset(self):
        return Category.objects.annotate(
            posts_count=Count(
                "posts",
                filter=Q(posts__status="PUBLISHED")
            )
        )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "slug"


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "slug"
    pagination_class = PostPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["is_featured"]
    search_fields = ["title", "excerpt", "content"]
    ordering_fields = [
        "published_at", "views_count", "title", "likes_count"
    ]

    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.annotate(
            likes_count=Count("likes", distinct=True),
            comments_count=Count(
                "comments",
                filter=Q(comments__is_approved=True),
                distinct=True
            )
        )

        is_owner = user.is_authenticated and user.is_superuser

        if not is_owner:
            queryset = queryset.filter(status="PUBLISHED")
        else:
            requested_status = self.request.query_params.get("status")
            if requested_status in ("DRAFT", "PUBLISHED"):
                queryset = queryset.filter(status=requested_status)

        category = self.request.query_params.get("category")
        tag = self.request.query_params.get("tag")

        if category:
            queryset = queryset.filter(category__slug=category)
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
