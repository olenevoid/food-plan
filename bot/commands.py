# Команды, обрабатывающие кнопки

from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import get_main_menu_keyboard, get_recipe_keyboard
import bot.strings as strings
import demodata.demo_db as db


# Функции будут потом переименованы или заменены. Пока они нужны для проверки кнопок
async def show_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    recipe = db.get_recipies()[0]

    await query.message.reply_text(
        strings.show_recipe(recipe),
        reply_markup=get_recipe_keyboard(),
        parse_mode="HTML",
    )


async def show_option2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.reply_text(
        strings.OPTION2, reply_markup=get_main_menu_keyboard(), parse_mode="HTML"
    )


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(
        strings.HELP_MESSAGE, reply_markup=get_main_menu_keyboard(), parse_mode="HTML"
    )


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.message.reply_text(
        strings.WELCOME_MESSAGE,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML",
    )
