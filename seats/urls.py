from rest_framework.routers import DefaultRouter
from . import views

app_name = "seats"

router = DefaultRouter()
router.register("", views.SeatsViewSet)
urlpatterns = router.urls
