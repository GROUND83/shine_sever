from rest_framework.routers import DefaultRouter
from . import views

app_name = "checks"

router = DefaultRouter()
router.register("", views.CheckViewSet)
urlpatterns = router.urls
