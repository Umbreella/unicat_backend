from rest_framework.permissions import BasePermission


class CreateAnyButEditAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True

        return bool(request.user and request.user.is_staff)
