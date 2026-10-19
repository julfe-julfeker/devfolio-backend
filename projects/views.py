
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from accounts.permissions import IsOwnerOrReadOnly
from .models import Project
from .serializers import ProjectSerializer


class ProjectPagination(PageNumberPagination):
    page_size = 9


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "slug"
    pagination_class = ProjectPagination

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    filterset_fields = ["category", "is_featured"]
    search_fields = ["title", "summary", "description"]
    ordering_fields = ["completed_date", "display_order"]

    def get_queryset(self):
        queryset = super().get_queryset()

        tech = self.request.query_params.get("tech")
        if tech:
            condition = Q(tech_stack__name__iexact=tech)
            if tech.isdigit():
                condition |= Q(tech_stack__id=int(tech))
            queryset = queryset.filter(condition).distinct()

        return queryset
