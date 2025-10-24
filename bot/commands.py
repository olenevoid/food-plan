# Команды, обрабатывающие кнопки

from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import get_main_menu_keyboard, get_recipe_keyboard
import bot.strings as strings
import demodata.demo_db as db
import random


# Функции будут потом переименованы или заменены. Пока они нужны для проверки кнопок
async def show_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    context.user_data["recipe_switches"] = 3
    recipes = db.get_recipies()
    recipe = random.choice(recipes)

    await query.message.reply_text(
        strings.show_recipe(recipe),
        reply_markup=get_recipe_keyboard(3),
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


async def another_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if "recipe_switches" not in context.user_data:
        context.user_data["recipe_switches"] = 3

    remaining_switches = context.user_data["recipe_switches"] - 1
    context.user_data["recipe_switches"] = remaining_switches

    # Удаляем предыдущее сообщение с рецептом
    await query.message.delete()

    # Выбираем случайный рецепт
    recipes = db.get_recipies()
    recipe = random.choice(recipes)

    # Отправляем новое сообщение с рецептом
    await query.message.reply_text(
        strings.show_recipe(recipe),
        reply_markup=get_recipe_keyboard(remaining_switches),
        parse_mode="HTML",
    )
