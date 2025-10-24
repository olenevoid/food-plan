from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .callbacks import Callback


def get_main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Показать рецепт", callback_data=Callback.SHOW_RECIPE),
            InlineKeyboardButton("Option 2", callback_data=Callback.OPTION2),
        ],
        [InlineKeyboardButton("Help", callback_data=Callback.HELP)],
    ]
    return InlineKeyboardMarkup(keyboard)


def get_recipe_keyboard(remaining_switches=3):
    keyboard = []

    if remaining_switches > 0:
        keyboard.append(
            [
                InlineKeyboardButton(
                    f"🔄 Доступно замен ({remaining_switches})",
                    callback_data=Callback.ANOTHER_RECIPE,
                )
            ]
        )
    keyboard.extend(
        [
            [
                InlineKeyboardButton("👍 Лайк", callback_data=Callback.LIKE_RECIPE),
                InlineKeyboardButton(
                    "👎 Дизлайк", callback_data=Callback.DISLIKE_RECIPE
                ),
            ],
            [
                InlineKeyboardButton(
                    "📋 Главное меню", callback_data=Callback.BACK_TO_MENU
                )
            ],
        ]
    )
    return InlineKeyboardMarkup(keyboard)
