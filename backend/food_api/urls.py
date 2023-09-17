from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    IngredienViewSet,
    RecipeViewSet,
    TagViewSet,
    UserViewSet,
    delete_token,
    obtain_auth_token,
)

app_name = 'api'
routerv1 = DefaultRouter()
routerv1.register('recipes', RecipeViewSet)
routerv1.register('ingredients', IngredienViewSet)
routerv1.register('tags', TagViewSet)
routerv1.register('users', UserViewSet)
urlpatterns = [
    path('', include(routerv1.urls)),
    path('auth/token/login/', obtain_auth_token),
    path('auth/token/logout/', delete_token),
]
