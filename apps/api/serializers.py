from collections import OrderedDict

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.recipes.models import Favorite, Follow, Ingredient, Recipe

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.StringRelatedField(source='unit.name')

    class Meta:
        model = Ingredient
        fields = ['name', 'unit', ]


class FavoriteSerializer(serializers.ModelSerializer):
    recipe_slug = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Recipe.objects.all(),
    )
    user = serializers.CharField(
        required=False,
    )

    class Meta:
        model = Favorite
        fields = ['recipe_slug', 'user']

    def create(self, validated_data):
        return Favorite.objects.create(
            recipe=validated_data['recipe_slug'],
            user=self.context['request'].user)

    def to_representation(self, instance):
        """
        To handle a response with new instance for each POST request
        """
        ret = OrderedDict()
        ret['recipe_slug'] = instance.recipe.slug
        ret['user'] = instance.user.username
        return ret


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                            source='author')

    class Meta:
        model = Follow
        fields = ['id', ]
