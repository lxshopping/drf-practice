from rest_framework.routers import DefaultRouter

from releases.views import ReleaseOrderViewSet

router = DefaultRouter()
router.register("release-orders", ReleaseOrderViewSet, basename="release-order")

urlpatterns = router.urls
