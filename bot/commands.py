# Команды, обрабатывающие кнопки

from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import get_main_menu_keyboard, get_recipe_keyboard
import bot.strings as strings
import demodata.demo_db as db
import random
import os


async def send_recipe_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    text: str,
    keyboard,
    image_path=None,
):
    """Универсальная функция для отправки сообщений с рецептами."""
    if update.callback_query:
        chat_id = update.callback_query.message.chat_id
    else:
        chat_id = update.message.chat_id

    if image_path and os.path.exists(image_path):
        # Сообщение с картинкой из файла
        with open(image_path, "rb") as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
    else:
        # Обычное текстовое сообщение
        await context.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode="HTML"
        )


# Функции будут потом переименованы или заменены. Пока они нужны для проверки кнопок
async def show_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    context.user_data["recipe_switches"] = 3
    recipes = db.get_recipies()
    recipe = random.choice(recipes)

    image_path = None

    await send_recipe_message(
        update=update,
        context=context,
        text=strings.show_recipe(recipe),
        keyboard=get_recipe_keyboard(3),
        image_path=image_path,
    )


async def show_option2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await send_recipe_message(
        update=update,
        context=context,
        text=strings.OPTION2,
        keyboard=get_main_menu_keyboard(),
        image_path=None,
    )


async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.edit_message_text(
        strings.HELP_MESSAGE, reply_markup=get_main_menu_keyboard(), parse_mode="HTML"
    )


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_recipe_message(
        update=update,
        context=context,
        text=strings.WELCOME_MESSAGE,
        keyboard=get_main_menu_keyboard(),
        image_path=None,
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

    image_path = None

    await send_recipe_message(
        update=update,
        context=context,
        text=strings.show_recipe(recipe),
        keyboard=get_recipe_keyboard(remaining_switches),
        image_path=image_path,
    )
