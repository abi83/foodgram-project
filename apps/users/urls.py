from django.urls import path, include

from apps.users.views import SignUp


app_name = 'users'
urlpatterns = [
    path('auth/', include("django.contrib.auth.urls")),
    path('signup/', SignUp.as_view(), name='signup')
]