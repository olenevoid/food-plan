from dataclasses import dataclass
from datetime import datetime


@dataclass
class PortionType:
    id: int
    title: str


@dataclass
class Ingredient:
    id: int
    title: str
    price: int
    portion_type: PortionType
    default_portion_size: int


@dataclass
class IngredientPortion:
    id: int
    ingredient: Ingredient
    portion_size: int
    portion_price: int #calculated field


@dataclass
class Recipe:
    id: int
    title: str
    instruction: str
    ingredients: list[IngredientPortion]


@dataclass
class DailyRecipe:
    id: int
    recipe: Recipe | None
    history: list[Recipe]
    history_limit: int = 5
    refresh_limit: int = 3
    refresh_count: int
    updated_at: datetime | None
    favorite_recipies: list[Recipe] | None
    disliked_recipies: list[Recipe] | None


@dataclass
class User:
    id: int
    tg_id: int
    name: str = ''
    daily_recipe: DailyRecipe
