from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.users.forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/registration_form.html'
