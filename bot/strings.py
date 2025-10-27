# Строки для бота.
# Указывайте {параметр}, если он необходим в строке
# Не забывайте про \n для переноса строки
# Также, работает HTML разметка для форматирования
# Поддерживаемые тэги ниже по ссылке
# https://core.telegram.org/bots/api#formatting-options


def get_welcome_message(user_data=None, cleared=False):
    """Формирует приветственное сообщение с информацией о черном списке"""
    if user_data is None:
        user_data = {}

    user_info = user_data.get("user_info", {})
    first_name = user_info.get("first_name", "")

    if first_name:
        base_message = f"🍽 <b>Добро пожаловать в FoodPlan, {first_name}!</b>\n\n"
    else:
        base_message = "🍽 <b>Добро пожаловать в FoodPlan!</b>\n\n"

    blacklist_count = user_data.get("blacklist_count", 0)
    refresh_limit = user_data.get("refresh_limit", 3)
    refresh_count = user_data.get("refresh_count", 0)
    remaining_refreshes = refresh_limit - refresh_count

    base_message = (
        "🍽 <b>Добро пожаловать в FoodPlan!</b>\n\n"
        "✨ Здесь мы поможем вам с планированием питания.\n"
        "• 🍳 Получайте рецепты на день\n"
        "• 🛒 Автоматический список покупок\n"
        "• 💰 Контроль бюджета на еду\n\n"
        "• 👍👎 Оценивайте рецепты - ставьте лайки и дизлайки\n\n"
        '🎯 Чтобы начать, нажмите кнопку "Показать рецепт" и мы предложим вам блюдо на сегодня!\n\n'
    )

    # Информация о черном списке или сообщение об очистке
    if cleared:
        base_message += "✅ <b>Черный список успешно очищен!</b>\n\n"
    elif blacklist_count > 0:
        base_message += f"🗑️ <b>Рецептов в черном списке:</b> {blacklist_count}\n\n"

    # Информация об обновлениях
    base_message += f"🔄 <b>Доступно обновлений:</b> {remaining_refreshes}\n\n"

    base_message += (
        "<i>Ваши оценки помогут нам предлагать рецепты, которые вам понравятся!</i>"
    )
    return base_message


def show_recipe(recipe: dict):
    # Добавляем пометку для любимых рецептов
    if recipe.get("is_favorite", False):
        text = f"⭐️ 🍳 <b>{recipe.get('title')}</b> ⭐️\n\n"
        text += "❤️ <i>Этот рецепт в вашем избранном!</i>\n\n"
    else:
        text = f"🍳 <b>{recipe.get('title')}</b>\n\n"

    text += "🛒 <b>Ингредиенты:</b>\n"
    for ingredient in recipe.get("ingredient_portions", []):
        portion_display = f"{ingredient.get('portion_size')} {ingredient.get('portion_type')} {ingredient.get('portion_price')} р."
        comment = ingredient.get("comment", "")
        if comment and comment.strip():  # Проверяем, что комментарий не пустой
            text += f"  • {ingredient.get('title')} - <i>{portion_display}</i>\n     <i>💡 {comment}</i>\n"
        else:
            text += f"  • {ingredient.get('title')} - <i>{portion_display}</i>\n"

    # Расчет общей стоимости если есть
    total_price = sum(
        ingredient.get("portion_price", 0)
        for ingredient in recipe.get("ingredient_portions", [])
    )
    if total_price > 0:
        text += f"\n💰 <b>Примерная стоимость:</b> {total_price:.2f} руб.\n"

    text += f"\n📝 <b>Приготовление:</b>\n\n"
    instructions = recipe.get("instruction", "")
    text += instructions

    # Добавляем надпись только если рецепт не в избранном
    if not recipe.get("is_favorite", False):
        text += "\n\n❤️ <i>Понравился рецепт? Сохраните его в избранное!</i>"

    text += "\n\n<b>При нажатии на 👎 потратится одна замена на вывод нового рецепта</b>"

    return text
