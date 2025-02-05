from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Разрешение на редактирование только для владельца """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class IsModeratorOrReadOnly(permissions.BasePermission):
    """ Разрешение на редактирование для модераторов, но без удаления """

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj.moderators.filter(id=request.user.id).exists()
