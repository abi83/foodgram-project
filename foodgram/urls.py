from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("django.contrib.auth.urls")),
    path('api/v1/', include('apps.api.urls', namespace='api')),
    path('', include('apps.recipes.urls', namespace='recipes')),
]

# TODO: django CDN storage
