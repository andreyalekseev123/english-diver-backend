from rest_framework.routers import SimpleRouter

from . import views

app_name = "training_api"

router = SimpleRouter()
router.register(
    "dictionary",
    views.DictionaryApiViewSet,
    basename="dictionary"
)
router.register(
    "categories",
    views.CategoryViewSet,
    basename="categories"
)
router.register(
    "words",
    views.WordsViewSet,
    basename="words"
)

urlpatterns = router.urls
