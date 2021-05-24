from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import (IngredientSerializer, FavoriteSerializer,
                                  SubscribeSerializer)
from apps.recipes.models import Ingredient, Favorite, Recipe, Follow, CartItem


class IngredientList(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if not query or len(query) >= 3:
            return super().get(request, *args, **kwargs)
        return Response([{'warning': 'Enter minimum 3 symbols for a hint'}, ])

    def get_queryset(self):
        """
        Returns a filtered queryset. A query 'foo bar' returns a queryset
        with 'foo' AND' 'bar' in the name of each ingredient
        """
        query = self.request.query_params.get('query')
        if query:
            words = self.request.query_params.get('query').split(' ')
            db_query = Q()
            for word in words:
                db_query &= Q(name__contains=word.lower())
            return Ingredient.objects.filter(db_query)[:30]
        return Ingredient.objects.all()


class FavoritesApi(generics.CreateAPIView, generics.DestroyAPIView):
    """
    Front request format: {"recipe_slug": "some-recipe-slug"}
    """
    serializer_class = FavoriteSerializer

    def get_object(self):
        return get_object_or_404(Favorite,
                                 recipe__slug=self.kwargs.get('recipe_slug'),
                                 user=self.request.user,)


class SubscriptionApi(generics.CreateAPIView, generics.DestroyAPIView):
    """
    Front request format: {"id": ":int"}
    id: id of an author to follow
    """
    serializer_class = SubscribeSerializer

    def get_object(self):
        return get_object_or_404(Follow,
                                 follower=self.request.user,
                                 author_id=self.kwargs.get('author_id'))

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)


class CartAPI(APIView):
    permission_classes = [AllowAny, ]
    resp_mesg = {
        status.HTTP_201_CREATED: 'successfully created',
        status.HTTP_400_BAD_REQUEST: 'recipe already in shop list',
        status.HTTP_200_OK: 'successfully deleted',
    }

    def post(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe,
                                   slug=request.data.get('recipe_slug'))
        if request.user.is_authenticated:
            _, created = CartItem.objects.get_or_create(
                user=self.request.user,
                recipe=recipe)
            if created:
                resp_status = status.HTTP_201_CREATED
                return Response({'status': self.resp_mesg[resp_status]},
                                status=resp_status)
            resp_status = status.HTTP_400_BAD_REQUEST
            return Response({'status': self.resp_mesg[resp_status]},
                            status=resp_status)
        if request.session.get('cart') is None:
            request.session['cart'] = [recipe.pk, ]
        else:
            if recipe.pk in request.session['cart']:
                resp_status = status.HTTP_400_BAD_REQUEST
                return Response({'status': self.resp_mesg[resp_status]},
                                status=resp_status)
            request.session['cart'].append(recipe.pk)
            request.session.modified = True
        resp_status = status.HTTP_201_CREATED
        return Response({'status': self.resp_mesg[resp_status]},
                        status=resp_status)

    def delete(self, request, *args, **kwargs):
        resp_status = status.HTTP_200_OK
        if request.user.is_authenticated:
            get_object_or_404(CartItem,
                              user=self.request.user,
                              recipe__slug=kwargs.get('recipe_slug'),
                              ).delete()
            return Response({'status': self.resp_mesg[resp_status]},
                            status=resp_status)
        recipe = get_object_or_404(Recipe, slug=kwargs.get('recipe_slug'))
        request.session['cart'].remove(recipe.pk)
        request.session.modified = True
        return Response({'status': self.resp_mesg[resp_status]},
                        status=resp_status)
