from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.core.views import HomeView, health_view

admin.site.site_header = "Legends of the Island administration"
admin.site.site_title = "Legends of the Island admin"
admin.site.index_title = "Editorial control panel"

urlpatterns = [
    path("health/", health_view, name="health"),
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", admin.site.urls),
]

urlpatterns += i18n_patterns(
    path("", HomeView.as_view(), name="home"),
    path("", include("apps.legends.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
