from rest_framework import viewsets
from common.permissions import IsOwnerOrAdmin, IsAdmin
from .models import Booking, Assignment, Review
from .serializers import BookingSerializer, AssignmentSerializer, ReviewSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    owner_field = 'customer'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        if hasattr(user, 'customer'):
            return Booking.objects.filter(offer__request__customer=user.customer)
        return Booking.objects.none()


class AssignmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer
    owner_field = 'provider'

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [IsOwnerOrAdmin()]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Assignment.objects.all()
        if hasattr(user, 'provider'):
            return Assignment.objects.filter(provider=user.provider)
        return Assignment.objects.none()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdmin]
    owner_field = 'customer'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Review.objects.all()
        if hasattr(user, 'customer'):
            return Review.objects.filter(booking__customer=user.customer)
        return Review.objects.none()

    def perform_create(self, serializer):
        serializer.save()