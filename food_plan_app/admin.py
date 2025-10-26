from django.contrib import admin
from .models import PortionType, Ingredient, IngredientPortion, Recipe, DailyRecipe, User


#admin.site.register(PortionType)
admin.site.register(IngredientPortion)
admin.site.register(DailyRecipe)
admin.site.register(User)


@admin.register(PortionType)
class PortionTypeAdmin(admin.ModelAdmin):
    list_display = ['title', 'title_short']
    search_fields = ['title', 'title_short']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['title', 'default_portion_size', 'portion_type', 'price']
    list_filter = ['portion_type']
    search_fields = ['title']
    list_select_related = ['portion_type']


class IngredientPortionInline(admin.TabularInline):
    model = IngredientPortion
    extra = 1
    fields = ['ingredient', 'portion_size', 'portion_type', 'portion_price', 'comment']
    readonly_fields = ['portion_price', 'portion_type']

    def portion_type(self, obj):
        return obj.ingredient.portion_type

    def portion_price(self, obj):
        return obj.portion_price

    portion_type.short_description = 'Единица измерения'
    portion_price.short_description = 'Цена'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'is_available']
    search_fields = ['title']
    inlines = [IngredientPortionInline]