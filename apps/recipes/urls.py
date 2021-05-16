from django.urls import path

from apps.recipes.views import RecipeCreate, RecipeDetail, RecipeEdit, IndexPage, AuthorRecipes, FavoriteRecipes, RecipeDelete, Feed, ShopList


app_name = 'recipes'
urlpatterns = [
    path('', IndexPage.as_view(), name='index'),
    path('new/', RecipeCreate.as_view(), name='recipe-create'),
    path('favorites/', FavoriteRecipes.as_view(), name='favorite-recipes'),
    path('feed/', Feed.as_view(), name='feed-recipes'),
    path('shoplist/', ShopList.as_view(), name='shop-list'),
    path('detail/<slug:slug>/', RecipeDetail.as_view(), name='recipe-detail'),
    path('detail/<slug:slug>/edit/', RecipeEdit.as_view(), name='recipe-edit'),
    path('detail/<slug:slug>/delete/', RecipeDelete.as_view(), name='recipe-delete'),
    path('author/<slug:username>/', AuthorRecipes.as_view(), name='author-detail'),
]
