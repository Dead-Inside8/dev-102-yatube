from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Разрешение: только автор может изменять объект"""

    def has_permission(self, request, view):
        # Разрешаем безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для создания и изменения требуется аутентификация
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Разрешаем безопасные методы всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешаем изменение только автору
        return obj.author == request.user