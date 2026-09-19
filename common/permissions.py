from rest_framework.permissions import BasePermission
from .roles import get_role

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_role(request.user) == 'admin'
