import os
import django
from django.db import transaction
from random import choice


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_plan.settings')
django.setup()

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


def find_serialized_user_by_tg_id(tg_id: int) -> dict | None:
    user = User.objects.filter(tg_id=tg_id).first()
    if user:
        return serializers.serialize_user(user)
    return None


def find_daily_recipe_by_tg_id(tg_id: int):
    user = User.objects.filter(tg_id=tg_id).first()
    if not user:
        return None

    daily_recipe = user.daily_recipe
    recipe = daily_recipe.recipe
    ingredient_portions = IngredientPortion.objects.filter(recipe__pk=recipe.pk)
    return serializers.serialize_daily_recipe(
        daily_recipe,
        recipe,
        ingredient_portions
    )


def get_recipe_pool_for_tg_id(tg_id):
    user = User.objects.filter(tg_id=tg_id).first()
    daily_recipe = user.daily_recipe

    blacklist_ids = daily_recipe.disliked_recipes.values_list('id', flat=True)
    history_ids = daily_recipe.history.values_list('id', flat=True)

    recipe_pool = list(
        Recipe.objects.exclude(pk__in=history_ids).exclude(pk__in=blacklist_ids).all()
    )

    favorite = list(daily_recipe.favorite_recipes.all())

    recipe_pool.extend(favorite)

    return recipe_pool


def update_history(tg_id: int):
    user = User.objects.filter(tg_id=tg_id).first()
    if user.daily_recipe.history.count() > user.daily_recipe.history_limit:
        user.daily_recipe.history.clear()
    else:
        user.daily_recipe.history.add(user.daily_recipe.recipe)
    user.daily_recipe.save()
@transaction.atomic
def add_user(tg_id: int, name: str):
    daily_recipe = DailyRecipe()
    daily_recipe.recipe = choice(Recipe.objects.all())
    daily_recipe.save()

    new_user = User()
    new_user.tg_id = tg_id
    new_user.name = name
    new_user.daily_recipe = daily_recipe

    new_user.save()
