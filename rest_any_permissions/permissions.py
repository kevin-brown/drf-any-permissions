from rest_framework.permissions import BasePermission


class AnyPermissions(BasePermission):
    
    def has_permission(self, request, view):
        return False
