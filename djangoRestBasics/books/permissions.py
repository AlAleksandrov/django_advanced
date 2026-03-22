from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj) -> bool:
        author_name = obj.autors.values_list('name', flat=True)
        return request.user and request.user.username in author_name