# Строки для бота.
# Указывайте {параметр}, если он необходим в строке
# Не забывайте про \n для переноса строки
# Также, работает HTML разметка для форматирования
# Поддерживаемые тэги ниже по ссылке
# https://core.telegram.org/bots/api#formatting-options


WELCOME_MESSAGE = "Welcome! Choose an option:"

OPTION1 = "You selected Option 1"

OPTION2 = "You selected Option 2"

HELP_MESSAGE = "Help message - here's how to use this bot..."


def show_recipe(recipe: dict):
    text = f"Название: {recipe.get('name')}\n"
    text += 'Ингредиенты:\n\n'
    for ingredient in recipe.get('ingredients'):
        text += f'{ingredient.get('title')} {ingredient.get('portion')}\n'
    text += recipe.get('instructions')

    return text
