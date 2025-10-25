# Строки для бота.
# Указывайте {параметр}, если он необходим в строке
# Не забывайте про \n для переноса строки
# Также, работает HTML разметка для форматирования
# Поддерживаемые тэги ниже по ссылке
# https://core.telegram.org/bots/api#formatting-options


def get_welcome_message(blacklist_count=0):
    """Формирует приветственное сообщение с информацией о черном списке"""
    base_message = (
        "🍽 <b>Добро пожаловать в FoodPlan!</b>\n\n"
        "✨ Здесь мы поможем вам с планированием питания.\n"
        "• 🍳 Получайте рецепты на день\n"
        "• 🛒 Автоматический список покупок\n"
        "• 💰 Контроль бюджета на еду\n\n"
        "• 👍👎 Оценивайте рецепты - ставьте лайки и дизлайки\n\n"
        '🎯 Чтобы начать, нажмите кнопку "Показать рецепт" и мы предложим вам блюдо на сегодня!\n\n'
    )

    # Добавляем информацию о черном списке, если есть рецепты
    if blacklist_count > 0:
        base_message += f"🗑️ <b>В черном списке:</b> {blacklist_count} рецепт(ов)\n\n"

    base_message += (
        "<i>Ваши оценки помогут нам предлагать рецепты, которые вам понравятся!</i>"
    )
    return base_message


OPTION1 = "You selected Option 1"

OPTION2 = "You selected Option 2"

HELP_MESSAGE = (
    "❓ <b>Помощь по использованию FoodPlan</b>\n\n"
    "• <b>Показать рецепт</b> - получить рецепт на сегодня\n"
    "• <b>Option 2</b> - функция\n"
    "• <b>Help</b> - показать это сообщение\n\n"
    "📝 <b>Система оценок:</b>\n"
    "   👍 - понравился рецепт (будем предлагать чаще)\n"
    "   👎 - не понравился (будем предлагать реже)\n\n"
)


def show_recipe(recipe: dict):
    text = f"🍳 <b>{recipe.get('title')}</b>\n\n"
    text += "🛒 <b>Ингредиенты:</b>\n"
    for ingredient in recipe.get("ingredient_portions", []):
        portion_display = (
            f"{ingredient.get('portion_size')} {ingredient.get('portion_type')}"
        )
        text += f"  • {ingredient.get('title')} - <i>{portion_display}</i>\n"
    text += f"\n📝 <b>Приготовление:</b>\n\n"
    instructions = recipe.get("instruction", "")
    text += instructions

    # Расчет общей стоимости
    total_price = sum(
        ingredient.get("portion_price", 0)
        for ingredient in recipe.get("ingredient_portions", [])
    )
    if total_price > 0:
        text += f"\n\n💰 <b>Примерная стоимость:</b> {total_price:.2f} руб."

    text += "\n\n❤️ <i>Понравился рецепт? Сохраните его в избранное!</i>"

    return text
