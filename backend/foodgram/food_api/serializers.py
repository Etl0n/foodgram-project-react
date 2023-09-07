from rest_framework import serializers

from .models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'colour',
            'slug',
        )
        read_only_fields = (
            'name',
            'colour',
            'slug',
        )


class IngredientReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), source='ingredient'
    )
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    '''author = serializers.StringRelatedField(read_only=True)'''

    tags = TagSerializer(many=True, source='recipe_tag_used', required=True)
    ingredients = IngredientSerializer(
        many=True, source='recipe_ingredient_used', required=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def create(self, validate_date):
        tags = validate_date.pop('tags')
        ingredients = validate_date.pop('recipe_ingredient_used')
        recipe = Recipe.objects.create(**validate_date)
        for ingredient in ingredients:
            current_ingredient = ingredient.get('ingredient')
            recipe.ingredients.add(
                current_ingredient,
                through_defaults={'amount': ingredient.get('amount')},
            )
        for tag in tags:
            RecipeTag.objects.create(tag=tag, recipe=recipe)
        return recipe


class RecipeReadSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=True)
    ingredients = IngredientSerializer(
        many=True, source='recipe_ingredient_used', required=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
