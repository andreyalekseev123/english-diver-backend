from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("management-center/", admin.site.urls),
    path("account/", include("apps.users.urls", namespace="users")),
    path("api/", include("config.urls.api")),
]


# for serving uploaded files on dev environment with django
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [
        path(r"__debug__/", include(debug_toolbar.urls, namespace="djdt")),
    ]
