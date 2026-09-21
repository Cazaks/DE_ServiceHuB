from rest_framework.permissions import BasePermission
from .roles import get_role
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_role(request.user) == 'admin'

class IsOwnerOrAdmin(BasePermission):
    """
        Object-level check: admins can access anything.
        Customers/providers can only access objects that belong to them,
        via an `owner_field` attribute the view must define
        (e.g. 'customer' or 'provider').
        """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        owner_field = getattr(view, 'owner_field', None)
        if owner_field is None:
            return False

        owner = getattr(obj, owner_field, None)
        user = request.user

        if hasattr(user, 'customer') and owner == user.customer:
            return True
        if hasattr(user, 'provider') and owner == user.provider:
            return True
        return False

class IsSelfOrAdmin(BasePermission):
    """
        For models where the object itself IS the user's profile
        (e.g. Customer, Provider) — checks obj.user == request.user directly.
        """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return get_role(request.user) == 'admin'
