from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet

app_name = 'api'
routerv1 = DefaultRouter()
routerv1.register('recipes', RecipeViewSet)
urlpatterns = [
    path('', include(routerv1.urls)),
]
