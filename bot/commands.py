# Команды, обрабатывающие кнопки

from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import get_main_menu_keyboard, get_recipe_keyboard
import bot.strings as strings
import demodata.demo_db as demo_db
import random
import os
from asgiref.sync import sync_to_async
from food_plan_app import db_requests as db
from datetime import datetime, timedelta


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
            short_text = parts[0]
            instruction_text = "📝 <b>Приготовление:</b>\n\n" + parts[1]
        else:
            short_text = text[:1000] + "..."
            instruction_text = text[1000:]

        if image_path and os.path.exists(image_path):
            # Отправляем фото с коротким текстом БЕЗ КНОПОК
            with open(image_path, "rb") as photo:
                message = await context.bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=short_text,
                    parse_mode="HTML",
                )
                message_ids.append(message.message_id)

            # Отправляем инструкцию отдельным сообщением С КНОПКАМИ
            instruction_message = await context.bot.send_message(
                chat_id=chat_id,
                text=instruction_text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            message_ids.append(instruction_message.message_id)
        else:
            # Если нет фото, отправляем два текстовых сообщения
            # Первое - без кнопок
            message1 = await context.bot.send_message(
                chat_id=chat_id,
                text=short_text,
                parse_mode="HTML",
            )
            message_ids.append(message1.message_id)

            # Второе - с кнопками
            message2 = await context.bot.send_message(
                chat_id=chat_id,
                text=instruction_text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            message_ids.append(message2.message_id)
    else:
        # Текст короткий, отправляем как обычно С КНОПКАМИ
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
                chat_id=chat_id,
                text=text,
                reply_markup=keyboard,
                parse_mode="HTML",
            )
            message_ids.append(message.message_id)

    return message_ids


async def clear_blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Проверяем, есть ли что очищать
    blacklist_count = context.user_data.get("blacklist_count", 0)

    if blacklist_count == 0:
        await query.answer("Черный список уже пуст!", show_alert=True)
        return

    

    # Для демо просто обнуляем
    context.user_data["blacklist_count"] = 0

    await query.edit_message_text(
        text=strings.get_welcome_message(context.user_data, cleared=True),
        reply_markup=get_main_menu_keyboard(context.user_data),
        parse_mode="HTML",
    )


async def show_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id #'55555555555' #update.effective_chat.id

    # Получаем сохраненную информацию о пользователе
    user_info = await sync_to_async(db.find_serialized_user_by_tg_id)(chat_id)
    user_id = user_info.get("id")
    first_name = user_info.get("first_name", "Пользователь")

    print(f"Показываем рецепт для пользователя: {first_name} (ID: {user_id})")

    refresh_limit = user_info.get("refresh_limit", 3)
    refresh_count = user_info.get("refresh_count", 0)
    remaining_refreshes = refresh_limit - refresh_count

    recipe = await sync_to_async(db.find_daily_recipe_by_tg_id)(chat_id)
    updated_at: datetime = recipe.get('updated_at')

    if not recipe:
        await sync_to_async(db.set_new_daily_recipe)(chat_id)
    if datetime.now().date() >= updated_at.date() + timedelta(days=1):
        await sync_to_async(db.update_history)(chat_id)
        await sync_to_async(db.set_new_daily_recipe)(chat_id)

    image_path = recipe.get('image_path')

    # Статус избранного рецепта
    is_favorite = recipe.get("is_favorite", False)

    message_ids = await send_recipe_message(
        update=update,
        context=context,
        text=strings.show_recipe(recipe),
        keyboard=get_recipe_keyboard(remaining_refreshes, is_favorite),
        image_path=image_path,
    )

    # Сохраняем ID сообщений рецепта для возможного удаления
    context.user_data["current_recipe_message_ids"] = message_ids


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_recipe_message(
        update=update,
        context=context,
        text=strings.get_welcome_message(context.user_data),
        keyboard=get_main_menu_keyboard(context.user_data),
        image_path=None,
    )


async def another_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id

    await sync_to_async(db.update_refresh_counter)(chat_id)
    await sync_to_async(db.update_history)(chat_id)
    await sync_to_async(db.set_new_daily_recipe)(chat_id)

    # Удаляем все сообщения текущего рецепта
    if "current_recipe_message_ids" in context.user_data:
        chat_id = query.message.chat_id
        for message_id in context.user_data["current_recipe_message_ids"]:
            try:
                await context.bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")

    await show_recipe(update, context)
