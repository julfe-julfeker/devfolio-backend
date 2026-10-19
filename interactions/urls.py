
from django.urls import path

from .views import (
    CommentListCreateView,
    CommentModerationView,
    CommentInboxView,
    ContactCreateView,
    ContactInboxView,
    ContactDetailView,
    PostLikeToggleView,
    DashboardStatsView,
)

urlpatterns = [
    path(
        "comments/",
        CommentListCreateView.as_view(),
        name="comments",
    ),
    path(
        "comments/inbox/",
        CommentInboxView.as_view(),
        name="comment-inbox",
    ),
    path(
        "comments/<int:pk>/",
        CommentModerationView.as_view(),
        name="comment-moderation",
    ),
    path(
        "contact/",
        ContactCreateView.as_view(),
        name="contact",
    ),
    path(
        "messages/",
        ContactInboxView.as_view(),
        name="messages",
    ),
    path(
        "messages/<int:pk>/",
        ContactDetailView.as_view(),
        name="message-detail",
    ),
    path(
        "posts/<slug:slug>/like/",
        PostLikeToggleView.as_view(),
        name="post-like",
    ),
    path(
        "dashboard/stats/",
        DashboardStatsView.as_view(),
        name="dashboard-stats",
    ),
]
