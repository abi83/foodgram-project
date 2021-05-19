from collections import OrderedDict

from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.recipes.models import Ingredient, Favorite, Recipe, Follow

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    unit = serializers.StringRelatedField()

    class Meta:
        model = Ingredient
        fields = ['name', 'unit', ]


class FavoriteSerializer(serializers.ModelSerializer):
    recipe_slug = serializers.SlugRelatedField(slug_field='slug',
                                               queryset=Recipe.objects.all())
    user = serializers.CharField(required=False)

    class Meta:
        model = Favorite
        fields = ['recipe_slug', 'user']

    def create(self, validated_data):
        return Favorite.objects.create(recipe=validated_data['recipe_slug'],
                                       user=self.context['request'].user)

    def to_representation(self, instance):
        ret = OrderedDict()
        ret['recipe_slug'] = instance.recipe.slug
        ret['user'] = instance.user.username
        return ret


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    def create(self, validated_data):
        return Follow.objects.create(follower=self.context['request'].user,
                                     author=validated_data['id'])



    class Meta:
        model = Follow
        fields = ['id', ]