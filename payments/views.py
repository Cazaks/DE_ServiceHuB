from rest_framework import viewsets
from common.permissions import IsOwnerOrAdmin, IsAdmin
from .models import CustomerPayment, ProviderPayout
from .serializers import CustomerPaymentSerializer, ProviderPayoutSerializer


class CustomerPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerPaymentSerializer
    owner_field = 'customer'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return CustomerPayment.objects.all()
        if hasattr(user, 'customer'):
            return CustomerPayment.objects.filter(booking__customer=user.customer)
        return CustomerPayment.objects.none()


class ProviderPayoutViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderPayoutSerializer
    owner_field = 'provider'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ProviderPayout.objects.all()
        if hasattr(user, 'provider'):
            return ProviderPayout.objects.filter(assignment__provider=user.provider)
        return ProviderPayout.objects.none()