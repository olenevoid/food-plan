from django.db import models
from django.core.validators import MinValueValidator


class PortionType(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    title_short = models.CharField(max_length=10, verbose_name='Сокращение')

    class Meta:
        verbose_name = "Единица измерения порции"
        verbose_name_plural = "Единицы измерения порций"
    
    def __str__(self):
        return self.title


class Ingredient(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')        
    default_portion_size = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Размер порции')
    portion_type = models.ForeignKey(PortionType, on_delete=models.CASCADE, verbose_name='Единица измерения')
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='Цена')
    
    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.title


class Recipe(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    instruction = models.TextField(verbose_name='Инструкция')
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='images/',
        null=True,
        blank=True
    )
    ingredients = models.ManyToManyField(
        Ingredient, 
        through='IngredientPortion',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты'
    )
    
    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title


class IngredientPortion(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    portion_size = models.IntegerField(validators=[MinValueValidator(1)], verbose_name='Размер порции')
    comment = models.CharField(max_length=255, verbose_name='Комментарий', blank=True)
    
    class Meta:
        verbose_name = "Порция ингредиента"
        verbose_name_plural = "Порции ингредиентов"
        unique_together = ['ingredient', 'recipe']
    
    def __str__(self):
        return f"{self.ingredient.title} - {self.portion_size}"
    
    @property
    def portion_price(self):
        """Calculated field: price for this specific portion size"""
        return (self.ingredient.price * self.portion_size) / self.ingredient.default_portion_size


class DailyRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='daily_recipe'
    )
    history = models.ManyToManyField(
        Recipe, 
        related_name='historical_daily_occurrences',
        blank=True
    )
    history_limit = models.IntegerField(default=5)
    refresh_limit = models.IntegerField(default=3, validators=[MinValueValidator(1)])
    refresh_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    favorite_recipes = models.ManyToManyField(
        Recipe, 
        related_name='favorited',
        blank=True
    )
    disliked_recipes = models.ManyToManyField(
        Recipe, 
        related_name='disliked',
        blank=True
    )
    
    class Meta:
        verbose_name = "Ежедневный рецепт"
        verbose_name_plural = "Ежедневные рецепты"

    def __str__(self):
        return f"Daily Recipe - {self.updated_at.date()} {self.user.name}"


class User(models.Model):
    tg_id = models.BigIntegerField(unique=True, verbose_name='Телеграм id')
    name = models.CharField(max_length=255, blank=True, verbose_name='Имя пользователя')
    daily_recipe = models.OneToOneField(
        DailyRecipe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user',
        verbose_name='Предложенный рецепт'
    )
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.name if self.name else f"User {self.tg_id}"