from django import forms

from recipes.models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        exclude = ['pub_date', 'slug', 'author', 'ingredients', ]
        widgets = {'tags': forms.CheckboxSelectMultiple(), }
