from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, AssignmentViewSet, ReviewViewSet

router = DefaultRouter()
router.register('bookings', BookingViewSet)
router.register('assignments', AssignmentViewSet)
router.register('reviews', ReviewViewSet)

urlpatterns = router.urls