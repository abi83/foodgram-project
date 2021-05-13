from django.urls import path, include
from rest_framework.routers import DefaultRouter


from . import views


app_name = 'api'
urlpatterns = [
    path('ingredients/', views.IngredientList.as_view(), name='ingredient-api'),
]

router = DefaultRouter()
router.register(prefix='favorites', viewset=views.FavoritesApi, basename='users')

urlpatterns += [
    path('', include(router.urls)),
]