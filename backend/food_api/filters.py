import django_filters
from recipe.models import FavoriteRecipe, Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags__slug')
    is_favorited = django_filters.NumberFilter(
        field_name='is_favorite', method='is_favorited_recipe'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def is_favorited_recipe(self, queryset, name, value):
        value = int(value)
        if (value == 1) and self.request.user.is_authenticated:
            id_recipe = FavoriteRecipe.objects.filter(user=self.request.user)
            id_recipe = [recipe.recipe.id for recipe in id_recipe]
            return queryset.filter(id__in=id_recipe)
        return queryset.filter(**{name: value})
