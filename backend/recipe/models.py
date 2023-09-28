from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=270)
    measurement_unit = models.CharField(max_length=270)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)
    colour = models.CharField(max_length=20)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200, unique=True)
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
    pub_day = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredient_used'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient_used'
    )
    amount = models.IntegerField()

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='uniqe_ingredient_in_recipe',
            ),
        )


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='is_favorite'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='uniqe_recipe_of_user'
            ),
        )


class SubscriptAuthor(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sub_on_author'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sub_author'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'), name='uniqe_subscript'
            ),
        )


class RecipeInShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='is_in_shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='is_in_shopping_cart'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'), name='uniqe_shopping_cart'
            ),
        )
