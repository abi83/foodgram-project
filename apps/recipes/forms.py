from django.forms import ModelForm

from apps.recipes.models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        exclude = ('slug', )