from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """Разрешает изменять объекты только их владельцам."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerator(permissions.BasePermission):
    """Разрешает модераторам только просматривать и редактировать."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()
