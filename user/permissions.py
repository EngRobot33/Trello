from rest_framework import permissions

from .models import User


class IsProjectManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.role == User.PROJECT_MANAGER
        )


class IsDeveloper(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.role == User.DEVELOPER
        )
