from django.urls import path

from . import views


app_name = 'recipes'
urlpatterns = [
    path('',
         views.IndexPage.as_view(),
         name='index'),
    path('detail/<slug:slug>', views.RecipeDetail.as_view(), name='recipe-detail'),
    path('detail/<slug:slug>/edit/', views.RecipeEdit.as_view(), name='recipe-edit'),
    # path('detail/<slug:slug>/eidt/', views.RecipeCreate.as_view(), name='recipe-create'),
    path('author/<slug:username>/', views.AuthorDetail.as_view(), name='author-detail'),
]
