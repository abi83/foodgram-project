from rest_framework import generics
from apps.recipes.models import Ingredient
from apps.api.serializers import IngredientSerializer
from django.db.models import Q
from rest_framework.response import Response


class IngredientList(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get(self, request, *args, **kwargs):
        if len(request.query_params.get('query')) >= 3:
            return super().get(request, *args, **kwargs)
        return Response([{'warning': 'Enter minimum 3 symbols for a hint'}, ])

    def get_queryset(self):
        """
        Returns a filtered queryset. A query 'foo bar' returns a queryset
        with 'foo' AND' 'bar' in the name of each ingredient
        """
        words = self.request.query_params.get('query').split(' ')
        db_query = Q()
        for word in words:
            db_query &= Q(name__contains=word.lower())
        return Ingredient.objects.all().filter(db_query)[:30]
