from django.views.generic import ListView, DetailView

from apps.recipes.models import Recipe


class IndexPage(ListView):
    template_name = 'recipes/index.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.all()


class RecipeDetail(DetailView):
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'
    model = Recipe