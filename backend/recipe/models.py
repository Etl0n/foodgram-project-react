from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=270)
    measurement_unit = models.CharField(max_length=270)


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
    tags = models.ManyToManyField(Tag, related_name='recipe')
    text = models.TextField()
    cooking_time = models.IntegerField()


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredient_used'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient_used'
    )
    amount = models.IntegerField()


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='favorite'
    )


class SubscriptAuthor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sub_on_author'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sub_author'
    )
