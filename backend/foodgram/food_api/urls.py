from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredienViewSet, RecipeViewSet, TagViewSet

app_name = 'api'
routerv1 = DefaultRouter()
routerv1.register('recipes', RecipeViewSet)
routerv1.register('ingredients', IngredienViewSet)
routerv1.register('tags', TagViewSet)
urlpatterns = [
    path('', include(routerv1.urls)),
]
