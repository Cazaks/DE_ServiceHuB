from rest_framework import viewsets
from common.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin
from .models import ServiceCategory, ServiceRequest, ServiceOffer
from .serializers import ServiceCategorySerializer, ServiceRequestSerializer, ServiceOfferSerializer

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ServiceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsOwnerOrAdmin]
    owner_field = 'customer'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ServiceRequest.objects.all()
        if hasattr(user, 'customer'):
            return ServiceRequest.objects.filter(customer=user.customer)
        return ServiceRequest.objects.none()

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)


class ServiceOfferViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceOfferSerializer
    permission_classes = [IsOwnerOrAdmin]
    owner_field = 'customer'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ServiceOffer.objects.all()
        if hasattr(user, 'customer'):
            return ServiceOffer.objects.filter(request__customer=user.customer)
        return ServiceOffer.objects.none()