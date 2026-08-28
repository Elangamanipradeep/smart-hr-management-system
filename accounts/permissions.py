from rest_framework.permissions import BasePermission


class IsAdminOrHR(BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(
            name__in=["Admin", "HR"]
        ).exists()


class IsAdmin(BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(
            name="Admin"
        ).exists()