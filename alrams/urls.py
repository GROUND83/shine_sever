from rest_framework.routers import DefaultRouter
from . import views

app_name = "alrams"

router = DefaultRouter()
router.register("", views.AlramViewSet)
urlpatterns = router.urls
