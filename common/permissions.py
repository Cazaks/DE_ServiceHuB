from rest_framework.permissions import BasePermission
from .roles import get_role

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
        role = get_role(request.user)
        if role == 'admin':
            return True

        owner_field = getattr(view, 'owner_field', None)
        if owner_field is None:
            return False

        owner = getattr(obj, 'owner_field', None)
        if role == 'customer':
            return owner == request.user.customer

        if role == 'provider':
            return owner == request.user.provider

        return False
