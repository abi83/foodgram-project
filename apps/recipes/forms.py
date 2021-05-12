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
            'tag_breakfast': forms.CheckboxInput(attrs={'class': 'tags__checkbox tags__checkbox_style_orange'}),
            'tag_lunch': forms.CheckboxInput(attrs={'class': 'tags__checkbox tags__checkbox_style_green'}),
            'tag_dinner': forms.CheckboxInput(attrs={'class': 'tags__checkbox tags__checkbox_style_purple'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form__file'}),
        }
