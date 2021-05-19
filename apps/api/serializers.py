from rest_framework import serializers
from apps.recipes.models import Ingredient, Favorite


class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.StringRelatedField()

    class Meta:
        model = Ingredient
        fields = ['name', 'unit', ]
