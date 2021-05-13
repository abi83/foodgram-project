from django.db.models import Q
from rest_framework import generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.urlpatterns import format_suffix_patterns


from apps.api.serializers import IngredientSerializer, FavoriteSerializer
from apps.recipes.models import Ingredient, Favorite


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


# class FavoritesApi(generics.CreateAPIView, mixins.DestroyModelMixin):
#     pass

class FavoritesApi(
    # generics.GenericAPIView,
    # viewsets.ViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    # mixins.ListModelMixin,
    # mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Endpoint for creating or deleting Favorite instance
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    http_method_names = ['delete', 'post', 'head', 'options', 'get',]
    permission_classes = [AllowAny,
                          # IsAuthenticated,
                          ]

    def create(self, request, *args, **kwargs):

        # breakpoint()
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        breakpoint()
        return super().destroy(request, *args, **kwargs)