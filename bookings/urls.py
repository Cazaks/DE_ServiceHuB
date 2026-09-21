from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, AssignmentViewSet, ReviewViewSet

router = DefaultRouter()
router.register('bookings', BookingViewSet, basename='booking')
router.register('assignments', AssignmentViewSet, basename='assignment')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = router.urls