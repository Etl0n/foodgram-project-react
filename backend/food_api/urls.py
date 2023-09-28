from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredienViewSet,
    RecipeViewSet,
    Subscriptions,
    TagViewSet,
    UserViewSet,
    delete_token,
    download_shopping_cart,
    favorite,
    is_in_shopping_cart,
    obtain_auth_token,
    subscribe,
)

app_name = 'api'
routerv1 = DefaultRouter()
routerv1.register('recipes', RecipeViewSet, basename='recipes')
routerv1.register('ingredients', IngredienViewSet)
routerv1.register('tags', TagViewSet)
routerv1.register('users', UserViewSet)
urlpatterns = [
    path('users/subscriptions/', Subscriptions.as_view({'get': 'list'})),
    path('recipes/download_shopping_cart/', download_shopping_cart),
    path('', include(routerv1.urls)),
    re_path(r'recipes/(?P<recipe_id>[\d]+)/favorite/', favorite),
    re_path(
        r'recipes/(?P<recipe_id>[\d]+)/shopping_cart/', is_in_shopping_cart
    ),
    re_path(r'users/(?P<author_id>[\d]+)/subscribe/', subscribe),
    path('auth/token/login/', obtain_auth_token),
    path('auth/token/logout/', delete_token),
]
