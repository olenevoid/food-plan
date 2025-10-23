# Коллбэки для кнопок

from enum import StrEnum, auto


class Callback(StrEnum):
    MENU = auto()
    HELP = auto()
    SHOW_RECIPE = auto()
    OPTION2 = auto()
    LIKE_RECIPE = auto()
    DISLIKE_RECIPE = auto()
    BACK_TO_MENU = auto()
