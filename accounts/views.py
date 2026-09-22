from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from common.permissions import IsSelfOrAdmin
from common.roles import get_role
from .models import Customer, Provider, ProviderAgreement
from .serializers import (
    CustomerSerializer, ProviderSerializer, ProviderAgreementSerializer,
    CustomerRegistrationSerializer, ProviderRegistrationSerializer,
)
from drf_spectacular.utils import extend_schema


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]

    def get_queryset(self):
        role = get_role(self.request.user)
        if role == 'admin':
            return Customer.objects.all()
        if role == 'customer':
            return Customer.objects.filter(user=self.request.user)
        return Customer.objects.none()


class ProviderViewSet(viewsets.ModelViewSet):
    serializer_class = ProviderSerializer
    permission_classes = [IsAuthenticated, IsSelfOrAdmin]

    def get_queryset(self):
        role = get_role(self.request.user)
        if role == 'admin':
            return Provider.objects.all()
        if role == 'provider':
            return Provider.objects.filter(user=self.request.user)
        return Provider.objects.none()


class ProviderAgreementViewSet(viewsets.ModelViewSet):
    queryset = ProviderAgreement.objects.all()
    serializer_class = ProviderAgreementSerializer


class RegisterCustomerView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=CustomerRegistrationSerializer,
        responses={201: CustomerRegistrationSerializer},
    )
    def post(self, request):
        serializer = CustomerRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = serializer.save()
        token, _ = Token.objects.get_or_create(user=customer.user)
        return Response({'token': token.key, 'customer_id': customer.id}, status=status.HTTP_201_CREATED)


class RegisterProviderView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=ProviderRegistrationSerializer,
        responses={201: ProviderRegistrationSerializer},
    )
    def post(self, request):
        serializer = ProviderRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.save()
        token, _ = Token.objects.get_or_create(user=provider.user)
        return Response({'token': token.key, 'provider_id': provider.id}, status=status.HTTP_201_CREATED)