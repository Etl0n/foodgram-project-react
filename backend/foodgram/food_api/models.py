from django.contrib.auth import get_user_model
from django.db import models

UNIT_OF_MEASUREMENT = [('кг', 'киллограмм'), ('г', 'грамм')]

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=40)
    col = models.FloatField()
    unit_of_measurement = models.CharField(
        max_length=2, choices=UNIT_OF_MEASUREMENT
    )


class Tag(models.Model):
    name = models.CharField(max_length=20)
    colour = models.CharField(max_length=20)
    slug = models.SlugField()


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='recipes'
    )
    image = models.ImageField(upload_to='photo_recipe/', blank=True, null=True)
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', related_name='ingredient'
    )
    tags = models.ManyToManyField(
        Tag, through='RecipeTag', related_name='recipe'
    )
    text = models.TextField()
    cooking_time = models.IntegerField()


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_tag_used'
    )
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE, related_name='tag_used'
    )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredient_used'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient_used'
    )
    amount = models.IntegerField()
