from .models import (
    Ingredient,
    IngredientPortion,
    PortionType,
    Recipe,
    DailyRecipe,
    User
)


def serialize_recipe(
        recipe: Recipe,
        ingredient_portions: list[IngredientPortion]
):
    serialized_ingredient_portions = []

    for ingredient_portion in ingredient_portions:
        serialized_ingredient_portions.append(
            serialize_ingredient_portion(ingredient_portion)
        )
    image_path = recipe.image.path
    if not recipe.image:
        image_path = ''

    serialized_recipe = {
        'id': recipe.pk,
        'title': recipe.title,
        'ingredient_portions': serialized_ingredient_portions,
        'instruction': recipe.instruction,
        'image_path': image_path
    }

    return serialized_recipe


def serialize_ingredient_portion(ingredient_portion: IngredientPortion):
    serialized_ingredient_portion = {
        'id': ingredient_portion.pk,
        'title': ingredient_portion.ingredient.title,
        'portion_type': ingredient_portion.ingredient.portion_type.title_short,
        'portion_size': ingredient_portion.portion_size,
        'portion_price': round(ingredient_portion.portion_price, 2)
    }

    return serialized_ingredient_portion


def serialize_daily_recipe(
        daily_recipe: DailyRecipe,
        recipe: Recipe,
        ingredient_portions: list[IngredientPortion]
):
    serialized_recipe = serialize_recipe(recipe, ingredient_portions)

    is_favorite = recipe in daily_recipe.favorite_recipes.all()
    is_disliked = recipe in daily_recipe.disliked_recipes.all()

    serialized_recipe['is_favorite'] = is_favorite
    serialized_recipe['is_disliked'] = is_disliked
    serialized_recipe['refresh_limit'] = daily_recipe.refresh_limit
    serialized_recipe['refresh_count'] = daily_recipe.refresh_count
    serialized_recipe['updated_at'] = daily_recipe.updated_at

    return serialized_recipe


def serialize_user(user: User):
    serialized_user = {
        'id': user.pk,
        'name': user.name,
        'refresh_limit': user.daily_recipe.refresh_limit,
        'refresh_count': user.daily_recipe.refresh_count,
        'blacklist_count': user.daily_recipe.disliked_recipes.count()
    }

    return serialized_user
