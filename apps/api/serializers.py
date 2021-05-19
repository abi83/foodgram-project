from rest_framework import serializers
from django.contrib.auth import get_user_model
from collections import OrderedDict, defaultdict

from apps.recipes.models import Ingredient, Favorite, Recipe
User = get_user_model()

class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.StringRelatedField()

    class Meta:
        model = Ingredient
        fields = ['name', 'unit', ]


class FavoriteSerializer(serializers.ModelSerializer):
    recipe_slug = serializers.SlugRelatedField(slug_field='slug', queryset=Recipe.objects.all())
    user = serializers.CharField(required=False)

    class Meta:
        model = Favorite
        fields = ['recipe_slug', 'user']

    def create(self, validated_data):
        favorite = Favorite.objects.create(recipe=validated_data['recipe_slug'], user=User.objects.first())
        return favorite

    def to_representation(self, instance):
        ret = OrderedDict()
        ret['recipe_slug'] = instance.recipe.slug
        ret['user'] = instance.user.username
        return ret
