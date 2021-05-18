from django import forms

from apps.recipes.models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        tag_breakfast = cleaned_data.get('tag_breakfast')
        tag_lunch = cleaned_data.get('tag_lunch')
        tag_dinner = cleaned_data.get('tag_dinner')

        if not (tag_breakfast or tag_lunch or tag_dinner):
            msg = 'Check at least one tag'
            self.add_error('tag_breakfast', msg)
        return cleaned_data
    # TODO: validate minimum one ingredient is checked

    class Meta:
        model = Recipe
        exclude = ('slug', 'author', 'is_active',)
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form__input'},),
            'time': forms.TextInput(
                attrs={'class': 'form__input'}, ),
            'description': forms.Textarea(
                attrs={'class': 'form__textarea', 'rows': 8,}),
            'tag_breakfast': forms.CheckboxInput(
                attrs={'class': 'tags__checkbox tags__checkbox_style_orange'}),
            'tag_lunch': forms.CheckboxInput(
                attrs={'class': 'tags__checkbox tags__checkbox_style_green'}),
            'tag_dinner': forms.CheckboxInput(
                attrs={'class': 'tags__checkbox tags__checkbox_style_purple'}),
            'image': forms.ClearableFileInput(
                attrs={'class': 'form__file'}),
        }
