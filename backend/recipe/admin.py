from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    SubscriptAuthor,
    Tag,
)

User = get_user_model()


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'colour',
        'slug',
    )


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'ingredient',
        'measurement_unit',
    )
    list_filter = ('ingredient',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'tags',
        'author',
        'ingredients',
        'name',
        'image',
        'text',
        'cooking_time',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'recipe',
        'ingredient',
        'amount',
    )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'reicpe',
        'author',
    )


class SubscriptAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "first_name",
        "last_name",
        "password",
        "email",
    )
    list_filter = (
        'email',
        'name',
    )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(FavoriteRecipe, FavoriteAdmin)
admin.site.register(SubscriptAuthor, SubscriptAdmin)
admin.site.register(User, UserAdmin)
