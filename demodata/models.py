from dataclasses import dataclass
from datetime import datetime


@dataclass
class Ingredient:
    id: int
    title: str
    portion: str


@dataclass
class Tag:
    id: int
    title: str


@dataclass
class Recipe:
    id: int
    title: str
    instruction: str
    ingredients: list[Ingredient]
    tags: list[Tag] | None = None


@dataclass
class Subscription:
    id: int
    title: str
    subscribed_at: datetime
    subscribed_unti: datetime
    is_active: bool


@dataclass
class DailyRecipe:
    id: int
    recipe: Recipe | None
    history: list[Recipe]
    limit: int = 3
    updated_at: datetime | None
    favorite_recipies: list[Recipe] | None
    disliked_recipies: list[Recipe] | None


@dataclass
class User:
    id: int
    tg_id: int
    name: str = ''
    daily_recipe: DailyRecipe
