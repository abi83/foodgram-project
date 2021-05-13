from rest_framework import serializers
from apps.recipes.models import Ingredient, Favorite


class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.StringRelatedField()

    class Meta:
        model = Ingredient
        fields = ['name', 'unit', ]


class FavoriteSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(read_only=True, )

    class Meta:
        model = Favorite
        fields = ('recipe_id',)

