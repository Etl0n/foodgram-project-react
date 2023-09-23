import django_filters
from recipe.models import Recipe, Tag


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.ModelChoiceFilter(
        field_name="tags__slug", queryset=Tag.objects.all()
    )
    is_favorited = django_filters.BooleanFilter()

    class Meta:
        model = Recipe
        fields = ('tags',)
