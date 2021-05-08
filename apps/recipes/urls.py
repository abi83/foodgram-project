from django.urls import path

from . import views


app_name = 'recipes'
urlpatterns = [
    path('',
         views.IndexPage.as_view(),
         name='index'),
    path('detail/<slug:slug>', views.RecipeDetail.as_view(), name='recipe-detail')
]
