from rest_framework import serializers
from .models import Booking, Assignment, Review


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'offer', 'status', 'scheduled_at', 'customer_confirmed_at', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'booking', 'provider', 'payout_amount', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'booking', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at']