from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500  # noqa
from apps.recipes.views import Handler404, Handler500


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.recipes.urls', namespace='recipes')),
    path('api/', include('apps.api.urls', namespace='api')),
    path('user/', include('apps.users.urls')),
]

handler404 = Handler404.as_view() # noqa
handler500 = Handler500.as_view() # noqa


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
