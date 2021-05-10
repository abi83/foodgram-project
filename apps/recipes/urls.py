from django.urls import path

from apps.recipes.views import RecipeCreate, RecipeDetail, RecipeEdit, IndexPage, AuthorDetail


app_name = 'recipes'
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('new/', RecipeCreate.as_view(), name='recipe-create'),
    path('detail/<slug:slug>/', RecipeDetail.as_view(), name='recipe-detail'),
    path('detail/<slug:slug>/edit/', RecipeEdit.as_view(), name='recipe-edit'),
    path('author/<slug:username>/', AuthorDetail.as_view(), name='author-detail'),
]
