
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter

from portfolio.views import (
    ProfileView,
    SkillViewSet,
    ExperienceViewSet,
    EducationViewSet,
)
from projects.views import ProjectViewSet
from blog.views import (
    CategoryViewSet,
    TagViewSet,
    PostViewSet,
)

router = DefaultRouter()

router.register("skills", SkillViewSet, basename="skills")
router.register("experiences", ExperienceViewSet, basename="experiences")
router.register("education", EducationViewSet, basename="education")
router.register("projects", ProjectViewSet, basename="projects")
router.register("categories", CategoryViewSet, basename="categories")
router.register("tags", TagViewSet, basename="tags")
router.register("posts", PostViewSet, basename="posts")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/profile/", ProfileView.as_view()),
    path("api/", include("interactions.urls")),
    path("api/", include(router.urls)),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
