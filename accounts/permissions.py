
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = "Only the portfolio owner can modify this resource."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class IsOwner(BasePermission):
    message = "Only the portfolio owner can access this resource."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )
