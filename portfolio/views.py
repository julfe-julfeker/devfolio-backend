
from rest_framework import viewsets, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend

from accounts.permissions import IsOwnerOrReadOnly
from .models import Profile, Skill, Experience, Education
from .serializers import (
    ProfileSerializer,
    SkillSerializer,
    ExperienceSerializer,
    EducationSerializer,
)


class ProfileView(APIView):
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request):
        profile = Profile.objects.first()

        if not profile:
            return Response(
                {"detail": "Profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(
            profile, context={"request": request}
        )
        return Response(serializer.data)

    def patch(self, request):
        profile = Profile.objects.first()

        if not profile:
            return Response(
                {"detail": "Profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "is_featured"]
    search_fields = ["name"]
    ordering_fields = ["display_order", "proficiency", "name"]


class ExperienceViewSet(viewsets.ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [IsOwnerOrReadOnly]


class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsOwnerOrReadOnly]
