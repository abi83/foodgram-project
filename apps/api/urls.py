from django.urls import path

from . import views


app_name = 'api'
urlpatterns = [
    path('',
         views.IngredientList.as_view(),
         name='ingredient-api'),
]
