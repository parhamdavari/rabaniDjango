"""
URL configuration for static site generation.

This URL config is used during static site builds. It excludes
admin and rosetta URLs (not needed for static site) and uses
the static views instead of regular views.
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

# i18n patterns for the website using static views
urlpatterns = i18n_patterns(
    path('', include('website.urls_static')),
    prefix_default_language=True,
)

# Serve static and media files during development/build
if settings.DEBUG or settings.BUILD_STATIC:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)
