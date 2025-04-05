from rest_framework import permissions


class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.is_aluno == True:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True        
        return request.user.is_superuser
    
class IsProfessorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated or request.user.is_aluno == True:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        return request.user.is_professor    