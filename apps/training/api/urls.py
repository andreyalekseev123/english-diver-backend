from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

app_name = "training_api"

router = SimpleRouter()
router.register(
    "dictionary",
    views.DictionaryApiViewSet,
    basename="dictionary"
)

urlpatterns = router.urls
