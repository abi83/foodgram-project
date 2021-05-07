from django.urls import path, include, reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView

from apps.users.views import SignUp


# app_name = 'users'
urlpatterns = [
    path('auth/', include("django.contrib.auth.urls")),
    path('signup/', SignUp.as_view(), name='signup'),
    # path('password-change/', PasswordChangeView.as_view(success_url=reverse_lazy('users:password_change_done')), name='password_change'),
    # path('password_reset/', PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),

]
