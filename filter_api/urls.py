from django.urls import path

from . import views

urlpatterns = [
    path('',
         views.IngredientList.as_view(),
         name='posts'), ]