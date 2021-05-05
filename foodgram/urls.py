from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('filter/', include('apps.api.urls')),
]

# TODO: use namespace
# TODO: django CDN storage
