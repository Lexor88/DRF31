from rest_framework import permissions

class IsUserOrReadOnly(permissions.BasePermission):
    """ Разрешает пользователям редактировать только свой профиль """
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or obj == request.user

class IsModeratorReadOnly(permissions.BasePermission):
    """ Разрешает модераторам просматривать и редактировать пользователей, но не удалять """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name="moderators").exists()
