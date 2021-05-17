from django.urls import path

from apps.api.views import (IngredientList, FavoritesApi,
                            SubscriptionApi, CartAPI)

app_name = 'api'
urlpatterns = [
    path('ingredients/', IngredientList.as_view(),
         name='ingredient-api'),
    path('favorites/', FavoritesApi.as_view(),
         name='favorites-create',),
    path('favorites/<slug:recipe_slug>', FavoritesApi.as_view(),
         name='favorites-delete', ),
    path('subscriptions/', SubscriptionApi.as_view(),
         name='subscription-create', ),
    path('subscriptions/<int:author_id>', SubscriptionApi.as_view(),
         name='subscription-delete', ),
    path('cart/', CartAPI.as_view(),
         name='add-to-cart', ),
    path('cart/<slug:recipe_slug>', CartAPI.as_view(),
         name='remove-from-cart', )

]
