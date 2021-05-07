from django.shortcuts import render
from django.views.generic import ListView

from apps.recipes.models import Recipe

# print(request.session.get_session_cookie_age())
# print(request.session.get_expiry_age())


class IndexPage(ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.all()
