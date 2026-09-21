from rest_framework.routers import DefaultRouter
from .views import CustomerPaymentViewSet, ProviderPayoutViewSet

router = DefaultRouter()
router.register('customer-payments', CustomerPaymentViewSet, basename='customerpayment')
router.register('provider-payouts', ProviderPayoutViewSet, basename='providerpayout')

urlpatterns = router.urls