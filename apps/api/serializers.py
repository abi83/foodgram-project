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

    # Got a `TypeError` when calling `Favorite.objects.create()`.This may be because you have a
    # writable field on the serializer class that is not a valid argument to
    # `Favorite.objects.create()`.You may need to make the field read-only, or override the
    # FavoriteSerializer.create() method to handle this correctly.
    #
    # Original exception was:
    # Traceback(most recent call last):
    # File "C:\python\foodgram-project\venv\lib\site-packages\rest_framework\serializers.py", line
    # 939, in create instance = ModelClass._default_manager.create(**validated_data)
    #
    # File "C:\python\foodgram-project\venv\lib\site-packages\django\db\models\manager.py", line 85, in manager_method
    # return getattr(self.get_queryset(), name)(*args, **kwargs) File "C:\python\foodgram-project\venv\lib\site-packages\django\db\models\query.py", line
    # 451, in create obj = self.model(**kwargs) File "C:\python\foodgram-project\venv\lib\site-packages\django\db\models\base.py", line
    # 503, in __init__ raise TypeError("%s() got an unexpected keyword argument '%s'" % (cls.__name__, kwarg)) TypeError: Favorite()
    # got an unexpected keyword argument 'recipe_slug'



    def create(self, validated_data):
        return Favorite.objects.create(recipe=validated_data['recipe_slug'],
                                       user=self.context['request'].user)

    def to_representation(self, instance):
        ret = OrderedDict()
        ret['recipe_slug'] = instance.recipe.slug
        ret['user'] = instance.user.username
        return ret


class SubscribeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='author')

    # def create(self, validated_data):
    #     return Follow.objects.create(follower=self.context['request'].user,
    #                                  author=validated_data['id'])



    class Meta:
        model = Follow
        fields = ['id', ]