from rest_framework.routers import DefaultRouter
from .views import CustomerPaymentViewSet, ProviderPayoutViewSet

router = DefaultRouter()
router.register('customer-payments', CustomerPaymentViewSet)
router.register('provider-payouts', ProviderPayoutViewSet)

urlpatterns = router.urls