# Коллбэки для кнопок

from enum import StrEnum, auto


class Callback(StrEnum):
    MENU = auto()
    HELP = auto()
    SHOW_RECIPE = auto()
    OPTION2 = auto()
