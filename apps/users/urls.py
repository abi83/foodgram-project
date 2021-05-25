from django.urls import include, path

from apps.users.views import SignUp

urlpatterns = [
    path('auth/', include("django.contrib.auth.urls")),
    path('signup/', SignUp.as_view(), name='signup'),
]
