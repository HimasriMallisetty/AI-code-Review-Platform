from rest_framework.routers import DefaultRouter
from .views import CodeReviewViewSet

router = DefaultRouter()
router.register(r"reviews", CodeReviewViewSet, basename="review")

urlpatterns = router.urls
