from rest_framework.routers import DefaultRouter, SimpleRouter

from . import views

app_name = "dictionary_api"

router = SimpleRouter()
router.register("dictionary", views.DictionaryApiViewSet, basename="userword")

urlpatterns = router.urls
