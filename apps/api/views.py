from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.urlpatterns import format_suffix_patterns


from apps.api.serializers import IngredientSerializer, FavoriteSerializer
from apps.recipes.models import Ingredient, Favorite, Recipe, Follow, CartItem


class IngredientList(generics.ListAPIView):
    serializer_class = IngredientSerializer
    # filter_backends = None
    # TODO: create custom filter backend

    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        if not query or len(query) >= 3:
            return super().get(request, *args, **kwargs)
        # todo: return an error maybe?
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
            return Ingredient.objects.all().filter(db_query)[:30]
        return Ingredient.objects.all()


class FavoritesApi(generics.CreateAPIView, generics.DestroyAPIView):
    def post(self, request, *args, **kwargs):
        recipe = Recipe.objects.get(slug=request.data.get('recipe_slug'))
        Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        return Response({'status': 'successfully created'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        get_object_or_404(Favorite, recipe__slug=kwargs.get('recipe_slug'), user=request.user,).delete()
        return Response({'status': 'successfully deleted'}, status=status.HTTP_200_OK)


class SubscriptionApi(APIView):
    def post(self, request, *args, **kwargs):
        _, created = Follow.objects.get_or_create(follower=self.request.user, author_id=request.data.get('id'))
        if created:
            return Response({'status': 'successfully created'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'follow instance already exists'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        get_object_or_404(Follow, author_id=kwargs.get('author_id'), follower=request.user,).delete()
        return Response({'status': 'successfully deleted'}, status=status.HTTP_200_OK)


class CartAPI(APIView):
    pass
    # def post(self, request, *args, **kwargs):
    #     _, created = CartItem.objects.get_or_create(user=self.request.user, author_id=request.data.get('id'))
    #     if created:
    #         return Response({'status': 'successfully created'}, status=status.HTTP_201_CREATED)
    #     return Response({'status': 'follow instance already exists'}, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, *args, **kwargs):
    #     get_object_or_404(Follow, author_id=kwargs.get('author_id'), follower=request.user,).delete()
    #     return Response({'status': 'successfully deleted'}, status=status.HTTP_200_OK)
