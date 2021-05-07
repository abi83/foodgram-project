from django.urls import path, include

from . import views


app_name = 'users'
urlpatterns = [
    path('auth/', include("django.contrib.auth.urls")),
]
