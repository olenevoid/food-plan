# Коллбэки для кнопок

from enum import StrEnum, auto


class Callback(StrEnum):
    MENU = auto()
    SHOW_RECIPE = auto()
    LIKE_RECIPE = auto()
    DISLIKE_RECIPE = auto()
    BACK_TO_MENU = auto()
    ANOTHER_RECIPE = auto()
    CLEAR_BLACKLIST = auto()
    REMOVE_LIKE = auto()
