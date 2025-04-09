from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        # Apenas usuários autenticados podem acessar
        if not request.user.is_authenticated:
            return False

        # Todos os usuários autenticados podem ler
        if request.method in permissions.SAFE_METHODS:
            return True

        # Apenas superusuários podem criar, atualizar ou deletar
        return request.user.is_superuser


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
