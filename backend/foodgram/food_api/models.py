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
    image = models.ImageField(upload_to='photo_recipe/')
    ingredients = models.ManyToManyField(Ingredient)
    tags = models.ManyToManyField(Tag)
    text = models.TextField()
    cooking_time = models.IntegerField()
