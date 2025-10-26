from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .callbacks import Callback


def get_main_menu_keyboard(user_data=None):
    if user_data is None:
        user_data = {}

    keyboard = [
        [InlineKeyboardButton("Показать рецепт", callback_data=Callback.SHOW_RECIPE)]
    ]

    blacklist_count = user_data.get("blacklist_count", 0)

    if blacklist_count > 0:
        button_text = f"🗑️ Очистить черный список ({blacklist_count})"
        callback_data = Callback.CLEAR_BLACKLIST
    else:
        button_text = "🗑️ Черный список пуст"
        callback_data = Callback.CLEAR_BLACKLIST

    keyboard.append(
        [
            InlineKeyboardButton(
                button_text,
                callback_data=callback_data,
            )
        ]
    )

    return InlineKeyboardMarkup(keyboard)


def get_recipe_keyboard(remaining_switches=3, is_favorite=False):
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

    # Отображение лайка/дизлайка только если рецепт не в избранном

    if not is_favorite:
        keyboard.extend(
            [
                [
                    InlineKeyboardButton("👍 Лайк", callback_data=Callback.LIKE_RECIPE),
                    InlineKeyboardButton(
                        "👎 Дизлайк", callback_data=Callback.DISLIKE_RECIPE
                    ),
                ],
            ]
        )

    keyboard.append(
        [InlineKeyboardButton("📋 Главное меню", callback_data=Callback.BACK_TO_MENU)]
    )

    return InlineKeyboardMarkup(keyboard)
