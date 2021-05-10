from django import forms

from apps.recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ('slug', 'author', )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form__input'},),
            'time': forms.TextInput(attrs={'class': 'form__input'}, ),
            'description': forms.Textarea(attrs={'class': 'form__textarea', 'rows': 8,}),
        }
