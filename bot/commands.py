# Команды, обрабатывающие кнопки

from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import get_main_menu_keyboard
import bot.strings as strings
import demodata.demo_db as db


#Функции будут потом переименованы или заменены. Пока они нужны для проверки кнопок
async def show_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    recipe = db.get_recipies()[0]

    await query.edit_message_text(
        strings.show_recipe(recipe),
        reply_markup=get_main_menu_keyboard()
    )


async def show_option2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(strings.OPTION2, reply_markup=get_main_menu_keyboard())


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(strings.HELP_MESSAGE, reply_markup=get_main_menu_keyboard())
