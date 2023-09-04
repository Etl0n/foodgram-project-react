from rest_framework.viewsets import ModelViewSet

from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


'''    def perform_create(self, serializer):
        serializer.save(author=self.request.user)'''
