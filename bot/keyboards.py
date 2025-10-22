from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from .callbacks import Callback


def get_main_menu_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data=Callback.OPTION1),
            InlineKeyboardButton("Option 2", callback_data=Callback.OPTION2),
        ],
        [InlineKeyboardButton("Help", callback_data=Callback.HELP)],
    ]
    return InlineKeyboardMarkup(keyboard)