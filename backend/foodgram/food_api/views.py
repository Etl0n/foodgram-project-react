from recipe.models import Ingredient, Recipe, Tag
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .serializers import (
    IngredientReadSerializer,
    RecipeReadSerializer,
    RecipeSerializer,
    TagSerializer,
)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeSerializer


'''    def perform_create(self, serializer):
        serializer.save(author=self.request.user)'''


class IngredienViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientReadSerializer


class TagViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
