from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменять объекты только их владельцам.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешает модераторам редактировать, но не создавать и удалять курсы и уроки.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.groups.filter(name="moderators").exists()

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or request.user.groups.filter(name="moderators").exists()
