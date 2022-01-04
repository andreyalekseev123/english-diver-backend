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
router.register(
    "training-types",
    views.TrainingTypeViewSet,
    basename="training-types"
)

urlpatterns = router.urls
