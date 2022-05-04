from rest_framework.routers import DefaultRouter
from . import views

app_name = "notices"

router = DefaultRouter()
router.register("", views.NoticeViewSet)
urlpatterns = router.urls
