from rest_framework import permissions


class IsAdminOrIsNotAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_staff or not request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(obj.username is None or request.user.is_staff)


class IsOwnerOrIsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(request.user.is_authenticated or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            return bool(obj.user == request.user or request.user.is_staff)
        except:
            try:
                return bool(str(obj.author) == str(request.user) or request.user.is_staff)
            except:
                return bool(obj == request.user or request.user.is_staff)
