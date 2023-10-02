from django.conf import settings


def create_txt_with_ingredients(request):
    shopp_file = open(
        f'{settings.MEDIA_URL}backend.txt', "w+", encoding="utf-8"
    )
    shopp = request.user.is_in_shopping_cart.all()
    recipes = [recipe.recipe.recipe_ingredient_used.all() for recipe in shopp]
    shop = dict()
    for recipe in recipes:
        ingredients_amount = [
            [relate.ingredient, relate.amount] for relate in recipe
        ]
        for ingredient, amount in ingredients_amount:
            ingredient_keys = (
                f'{ingredient.name} {ingredient.measurement_unit}'
            )
            if ingredient_keys in shop.keys():
                shop[ingredient_keys] += amount
            else:
                shop[ingredient_keys] = amount
    for ingredient, amount in shop.items():
        shopp_file.write(f'{ingredient} {amount} \n')
