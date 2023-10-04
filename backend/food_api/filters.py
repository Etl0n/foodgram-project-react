import django_filters
from recipe.models import FavoriteRecipe, Recipe, RecipeInShoppingCart
from rest_framework import filters


def filter_by_recipe(request, queryset, name, value, use_class):
    value = int(value)
    if (value == 1) and request.user.is_authenticated:
        id_recipe = use_class.objects.filter(user=request.user)
        id_recipe = [recipe.recipe.id for recipe in id_recipe]
        return queryset.filter(id__in=id_recipe)
    return queryset.filter(**{name: value})


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.CharFilter(field_name='tags__slug')
    is_favorited = django_filters.NumberFilter(
        field_name='is_favorite', method='is_favorited_recipe'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        field_name='is_cart', method='is_in_shopping_cart_recipe'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author')

    def is_favorited_recipe(self, queryset, name, value):
        return filter_by_recipe(
            self.request, queryset, name, value, FavoriteRecipe
        )

    def is_in_shopping_cart_recipe(self, queryset, name, value):
        return filter_by_recipe(
            self.request, queryset, name, value, RecipeInShoppingCart
        )


class MySearchFilter(filters.SearchFilter):
    search_param = 'name'
