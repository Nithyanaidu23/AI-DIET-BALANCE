"""Custom permission classes for role-based authorization."""
from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """
    Permission check for Admin / Creator role.
    Allows access if user.role == 'admin', user.is_staff is True, or user.is_superuser is True.
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                getattr(request.user, 'role', '') == 'admin'
                or request.user.is_staff
                or request.user.is_superuser
            )
        )
