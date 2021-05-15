from django.urls import path, include
from rest_framework.routers import DefaultRouter


from . import views


app_name = 'api'
urlpatterns = [
    path('ingredients/', views.IngredientList.as_view(), name='ingredient-api'),
    path('favorites/', views.FavoritesApi.as_view(), name='favorites-create',),
    path('favorites/<slug:recipe_slug>', views.FavoritesApi.as_view(), name='favorites-delete', ),
    path('subscriptions/', views.Subscription.as_view(), name='subscription-create',),
    path('subscriptions/<int:author_id>', views.Subscription.as_view(), name='subscription-delete', )
]
