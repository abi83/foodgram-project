from django.urls import path

from apps.api.views import (CartAPI, FavoritesApi, IngredientList,
                            SubscriptionApi)

app_name = 'api'
urlpatterns = [
    path('v1/ingredients/', IngredientList.as_view(),
         name='ingredient-api'),
    path('v1/favorites/', FavoritesApi.as_view(),
         name='favorites-create',),
    path('v1/favorites/<slug:recipe_slug>/', FavoritesApi.as_view(),
         name='favorites-delete', ),
    path('v1/subscriptions/', SubscriptionApi.as_view(),
         name='subscription-create', ),
    path('v1/subscriptions/<int:author_id>/', SubscriptionApi.as_view(),
         name='subscription-delete', ),
    path('v1/cart/', CartAPI.as_view(),
         name='add-to-cart', ),
    path('v1/cart/<slug:recipe_slug>/', CartAPI.as_view(),
         name='remove-from-cart', )

]
