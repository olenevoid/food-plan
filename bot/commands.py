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

    message_ids = []

    # Если текст слишком длинный (больше 1024 символов)
    if len(text) > 1024:
        # Разделяем текст на название/ингредиенты и инструкцию
        parts = text.split("\n\n📝 <b>Приготовление:</b>\n\n")
        if len(parts) == 2:
            short_text = (
                parts[0]
                + "\n\n📝 <b>Приготовление продолжается в следующем сообщении...</b>"
            )
            instruction_text = "📝 <b>Приготовление:</b>\n\n" + parts[1]
        else:
            short_text = text[:1000] + "..."
            instruction_text = text[1000:]

        if image_path and os.path.exists(image_path):
            # Отправляем фото с коротким текстом
            with open(image_path, "rb") as photo:
                message = await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=short_text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )
                message_ids.append(message.message_id)

            # Отправляем инструкцию отдельным сообщением
            instruction_message = await context.bot.send_message(
                chat_id=chat_id, text=instruction_text, parse_mode="HTML"
            )
            message_ids.append(instruction_message.message_id)
        else:
            # Если нет фото, просто отправляем два текстовых сообщения
            message1 = await context.bot.send_message(
                chat_id=chat_id,
                text=short_text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            message_ids.append(message1.message_id)

            message2 = await context.bot.send_message(
                chat_id=chat_id, text=instruction_text, parse_mode="HTML"
            )
            message_ids.append(message2.message_id)
    else:
        # Текст короткий, отправляем как обычно
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as photo:
                message = await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=text,
                    reply_markup=keyboard,
                    parse_mode="HTML",
                )
                message_ids.append(message.message_id)
        else:
            message = await context.bot.send_message(
                chat_id=chat_id, text=text, reply_markup=keyboard, parse_mode="HTML"
            )
            message_ids.append(message.message_id)

    return message_ids


# Функции будут потом переименованы или заменены. Пока они нужны для проверки кнопок
async def show_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["recipe_switches"] = 3
    recipes = db.get_recipies()
    recipe = random.choice(recipes)

    image_path = (
        db.get_image_path(recipe["image_filename"])
        if recipe.get("image_filename")
        else None
    )

    message_ids = await send_recipe_message(
        update=update,
        context=context,
        text=strings.show_recipe(recipe),
        keyboard=get_recipe_keyboard(3),
        image_path=image_path,
    )

    # Сохраняем ID сообщений рецепта для возможного удаления
    context.user_data["current_recipe_message_ids"] = message_ids


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
    await query.answer()

    # Удаляем все сообщения текущего рецепта
    if "current_recipe_message_ids" in context.user_data:
        chat_id = query.message.chat_id
        for message_id in context.user_data["current_recipe_message_ids"]:
            try:
                await context.bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")

    if "recipe_switches" not in context.user_data:
        context.user_data["recipe_switches"] = 3

    remaining_switches = context.user_data["recipe_switches"] - 1
    context.user_data["recipe_switches"] = remaining_switches

    # Выбираем случайный рецепт
    recipes = db.get_recipies()
    recipe = random.choice(recipes)

    image_path = (
        db.get_image_path(recipe["image_filename"])
        if recipe.get("image_filename")
        else None
    )

    message_ids = await send_recipe_message(
        update=update,
        context=context,
        text=strings.show_recipe(recipe),
        keyboard=get_recipe_keyboard(remaining_switches),
        image_path=image_path,
    )

    context.user_data["current_recipe_message_ids"] = message_ids
