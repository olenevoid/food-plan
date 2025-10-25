from .models import (
    Ingredient,
    IngredientPortion,
    PortionType,
    Recipe,
    DailyRecipe,
    User
)
import food_plan_app.serializers as serializers


def get_all_recipes():
    return Recipe.objects.all()


def get_recipe_ingredients():
    recipe = Recipe.objects.first()
    return recipe.ingredient


def get_recipe_ingredient_portions(recipe_pk):
    return IngredientPortion.objects.filter(recipe__pk=recipe_pk)


def get_serialized_recipe(pk: int):
    recipe = Recipe.objects.get(pk=pk)
    ingrediend_portions = IngredientPortion.objects.filter(recipe__pk=pk)
    return serializers.serialize_recipe(recipe, ingrediend_portions)


def get_serialized_user(pk: int):
    user = User.objects.get(pk=pk)
    return serializers.serialize_user(user)


def find_user_by_tg_id(tg_id: int):
    user = User.objects.filter(tg_id=tg_id).first()
    return serializers.serialize_user(user)


def find_daily_recipe_by_tg_id(tg_id: int):
    user = User.objects.filter(tg_id=tg_id).first()
    daily_recipe = user.daily_recipe
    recipe = daily_recipe.recipe
    ingredient_portions = IngredientPortion.objects.filter(recipe__pk=recipe.pk)
    return serializers.serialize_daily_recipe(
        daily_recipe,
        recipe,
        ingredient_portions
    )
