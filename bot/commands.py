# Команды, обрабатывающие кнопки

from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import get_main_menu_keyboard, get_recipe_keyboard
import bot.strings as strings
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
    clear_previous=True,
):
    """Универсальная функция для отправки сообщений с рецептами."""
    # Удаляем предыдущие сообщения, если нужно
    if clear_previous:
        await delete_previous_messages(update, context)

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

    await add_message_to_history(context, message_ids)

    return message_ids


async def delete_previous_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет все предыдущие сообщения бота"""
    if "message_history" in context.user_data:
        chat_id = update.effective_chat.id

        for message_id in context.user_data["message_history"]:
            try:
                await context.bot.delete_message(chat_id, message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения {message_id}: {e}")

        # Очищаем историю
        context.user_data["message_history"] = []


async def add_message_to_history(context: ContextTypes.DEFAULT_TYPE, message_ids):
    """Добавляет сообщения в историю для последующего удаления"""
    if "message_history" not in context.user_data:
        context.user_data["message_history"] = []

    if isinstance(message_ids, list):
        context.user_data["message_history"].extend(message_ids)
    else:
        context.user_data["message_history"].append(message_ids)


async def show_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id

    # Получаем сохраненную информацию о пользователе
    user_info = await sync_to_async(db.find_serialized_user_by_tg_id)(chat_id)
    user_id = user_info.get("id")
    first_name = user_info.get("first_name", "Пользователь")

    print(f"Показываем рецепт для пользователя: {first_name} (ID: {user_id})")

    refresh_limit = user_info.get("refresh_limit", 3)
    refresh_count = user_info.get("refresh_count", 0)
    remaining_refreshes = refresh_limit - refresh_count

    recipe = await sync_to_async(db.find_daily_recipe_by_tg_id)(chat_id)
    updated_at: datetime = recipe.get("updated_at")

    if not recipe:
        await sync_to_async(db.set_new_daily_recipe)(chat_id)
    if datetime.now().date() >= updated_at.date() + timedelta(days=1):
        await sync_to_async(db.update_history)(chat_id)
        await sync_to_async(db.set_new_daily_recipe)(chat_id)
        await sync_to_async(db.reset_refresh_counter)(chat_id)
        recipe = await sync_to_async(db.find_daily_recipe_by_tg_id)(chat_id)

    context.user_data["last_recipe_id"] = recipe.get("id")

    image_path = recipe.get("image_path")

    # Статус избранного рецепта
    is_favorite = recipe.get("is_favorite", False)
    is_disliked = recipe.get("is_disliked", False)

    keyboard = get_recipe_keyboard(remaining_refreshes, is_favorite, is_disliked)

    await send_recipe_message(
        update=update,
        context=context,
        text=strings.show_recipe(recipe),
        keyboard=keyboard,
        image_path=image_path,
        clear_previous=True,
    )


async def back_to_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    user = await sync_to_async(db.find_serialized_user_by_tg_id)(chat_id)

    await send_recipe_message(
        update=update,
        context=context,
        text=strings.get_welcome_message(user),
        keyboard=get_main_menu_keyboard(user),
        image_path=None,
        clear_previous=True,
    )


async def another_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id

    user = await sync_to_async(db.find_serialized_user_by_tg_id)(chat_id)

    refresh_limit = user.get("refresh_limit", 3)
    refresh_count = user.get("refresh_count", 0)
    remaining_refreshes = refresh_limit - refresh_count

    if remaining_refreshes <= 0:
        return await show_no_refreshes(update, context)

    await sync_to_async(db.update_refresh_counter)(chat_id)
    await sync_to_async(db.update_history)(chat_id)
    await sync_to_async(db.set_new_daily_recipe)(chat_id)

    await show_recipe(update, context)


async def like_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id

    last_recipe_id = context.user_data.get("last_recipe_id")
    if last_recipe_id:
        await sync_to_async(db.add_liked_recipe)(chat_id, last_recipe_id)

    await show_recipe(update, context)


async def dislike_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id

    last_recipe_id = context.user_data.get("last_recipe_id")
    if last_recipe_id:
        await sync_to_async(db.add_disliked_recipe)(chat_id, last_recipe_id)

    await another_recipe(update, context)


async def clear_blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id

    await sync_to_async(db.clear_blacklist)(chat_id)

    user = await sync_to_async(db.find_serialized_user_by_tg_id)(chat_id)

    await send_recipe_message(
        update=update,
        context=context,
        text=strings.get_welcome_message(user, cleared=True),
        keyboard=get_main_menu_keyboard(user),
        image_path=None,
        clear_previous=True,
    )


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = await sync_to_async(db.find_serialized_user_by_tg_id)(chat_id)

    await send_recipe_message(
        update=update,
        context=context,
        text=strings.get_welcome_message(user),
        keyboard=get_main_menu_keyboard(user),
        image_path=None,
        clear_previous=True,
    )


async def show_no_refreshes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id

    user = await sync_to_async(db.find_serialized_user_by_tg_id)(chat_id)

    return await send_recipe_message(
        update=update,
        context=context,
        text=strings.NO_REFRESHES,
        keyboard=get_main_menu_keyboard(user),
        image_path=None,
        clear_previous=True,
    )


async def remove_like(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = update.effective_chat.id
    last_recipe_id = context.user_data.get("last_recipe_id")

    await sync_to_async(db.remove_liked_recipe)(chat_id, last_recipe_id)

    await show_recipe(update, context)
