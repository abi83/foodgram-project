from rest_framework import generics
from apps.recipes.models import Ingredient
from apps.api.serializers import IngredientSerializer


class IngredientList(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Ingredient.objects.all()
        query = self.request.query_params.get('query')
        if query is not None:
            print(query)
            queryset = queryset.filter(name__contains=query)
        return queryset
