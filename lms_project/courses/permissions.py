from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Разрешает изменять объекты только их владельцам.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsModerator(permissions.BasePermission):
    """
    Разрешает модераторам только просматривать и редактировать, но запрещает создание и удаление.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Запрещаем модераторам создание (POST) и удаление (DELETE)
        if request.user.groups.filter(name="moderators").exists():
            return request.method in ['PUT', 'PATCH']

        return not request.user.groups.filter(name="moderators").exists()

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.groups.filter(name="moderators").exists():
            return request.method in ['PUT', 'PATCH']

        return obj.owner == request.user
