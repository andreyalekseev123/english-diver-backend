from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("management-center/", admin.site.urls),
    path("api/user/", include("apps.users.api.urls", namespace="users_api")),
    path("account/", include("apps.users.urls", namespace="users")),
    
    # swagger paths
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc"
    ),
]


# for serving uploaded files on dev environment with django
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [
        path(r"__debug__/", include(debug_toolbar.urls, namespace="djdt")),
    ]
