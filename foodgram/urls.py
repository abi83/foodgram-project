from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/', include("django.contrib.auth.urls")),
    path('api/v1/', include('apps.api.urls', namespace='api')),
    path('', include('apps.recipes.urls', namespace='recipes')),
    path('user/', include('apps.users.urls', namespace='users')),
]

# TODO: django CDN storage
