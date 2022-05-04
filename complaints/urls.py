from rest_framework.routers import DefaultRouter
from . import views

app_name = "complaints"

router = DefaultRouter()
router.register("", views.ComplaintViewSet)
urlpatterns = router.urls
