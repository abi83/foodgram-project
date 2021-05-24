from django import forms

from apps.recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
        # TODO: validate minimum one ingredient is checked
    tags = forms.CheckboxSelectMultiple()

    class Meta:
        model = Recipe
        exclude = ('slug', 'author', 'is_active',)
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form__input'},),
            'time': forms.TextInput(
                attrs={'class': 'form__input'}, ),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': 8, }),
            'tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'tags__checkbox'}),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form__file'}),
        }
