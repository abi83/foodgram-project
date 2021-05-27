from django import forms

from apps.recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    tags = forms.CheckboxSelectMultiple()

    def clean(self):
        """
        'nameIngredient_1': ['курдючное сало'],
        'valueIngredient_1': ['22'],
        'unitsIngredient_1': ['г']
        """
        for key, value in self.data.items():
            if key.startswith('valueIngredient_') and int(value) <= 0:
                msg = 'Количество ингредиента должно быть положительным'
                self.add_error('ingredients', msg)

        cleaned_data = super().clean()
        if not cleaned_data.get('tags'):
            msg = 'Check at least one tag'
            self.add_error('tags', msg)
        return cleaned_data

    class Meta:
        model = Recipe
        exclude = ('slug', 'author', 'is_active',)
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form__input'},),
            'time': forms.TextInput(
                attrs={'class': 'form__input', }, ),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': 8, }),
            'tags': forms.CheckboxSelectMultiple(
                attrs={'class': 'tags__checkbox'}),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form__file'}),
        }
