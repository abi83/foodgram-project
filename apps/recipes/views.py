from django.views.generic import ListView, DetailView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from apps.recipes.models import Recipe
User = get_user_model()

class IndexPage(ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.all()


class RecipeDetail(DetailView):
    template_name = 'recipes/recipe-detail.html'
    context_object_name = 'recipe'
    model = Recipe


class AuthorDetail(DetailView):
    template_name = 'recipes/author-page.html'
    context_object_name = 'author'
    model = User

    def get_queryset(self):
        return User.objects.filter(is_active=True) #.select_related('recipes')

    def get_object(self, queryset=None):
        # breakpoint()
        if queryset is None:
            queryset = self.get_queryset()
        username = self.kwargs.get('username')
        author = get_object_or_404(queryset, username=username)
        return author



    # def get_context_data(self, **kwargs):
    #     context = {}
    #     if self.object:
    #         context['object'] = self.object
    #         context_object_name = self.get_context_object_name(self.object)
    #         if context_object_name:
    #             context[context_object_name] = self.object
    #     context.update(kwargs)
    #     return super().get_context_data(**context)