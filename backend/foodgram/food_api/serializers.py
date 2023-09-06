from rest_framework import serializers

from .models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'colour', 'slug')


class IngredientReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id', read_only=True)
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    '''author = serializers.StringRelatedField(read_only=True)'''

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

    def create(self, validate_date):
        tags = validate_date.pop('tags')
        ingredients = validate_date.pop('ingredients')
        recipe = Recipe.objects.create(**validate_date)
        for ingredient in ingredients:
            current_ingredient, status = Ingredient.objects.get_or_create(
                **ingredient
            )
            RecipeIngredient.objects.create(
                ingredient=current_ingredient, recipe=recipe
            )
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(**tag)
            RecipeTag.objects.create(tag=current_tag, recipe=recipe)
        return recipe
