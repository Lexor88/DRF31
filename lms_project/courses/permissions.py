from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешает изменять объекты только их владельцам.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsModeratorReadOnly(permissions.BasePermission):
    """
    Разрешает модераторам только просматривать и редактировать, но запрещает создание и удаление.
    """
    def has_permission(self, request, view):
        # Разрешаем GET, HEAD, OPTIONS для всех авторизованных
        if request.method in permissions.SAFE_METHODS:
            return True
        # Проверяем, что пользователь не модератор и метод не запрещен
        if request.user.groups.filter(name="moderators").exists():
            return request.method in ['GET', 'PUT', 'PATCH']
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.groups.filter(name="moderators").exists():
            return request.method in ['GET', 'PUT', 'PATCH']
        return False
