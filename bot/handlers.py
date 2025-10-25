from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import get_main_menu_keyboard
from .callbacks import Callback
import bot.strings as strings
import bot.commands as commands


CALLBACK_COMMANDS = {
    Callback.SHOW_RECIPE: commands.show_recipe,
    Callback.BACK_TO_MENU: commands.back_to_menu,
    Callback.ANOTHER_RECIPE: commands.another_recipe,
    Callback.CLEAR_BLACKLIST: commands.clear_blacklist,
}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем информацию о пользователе
    user = update.effective_user
    chat_id = update.effective_chat.id

    # Сохраняем в user_data
    context.user_data["user_info"] = {
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "chat_id": chat_id,
    }

    context.user_data["blacklist_count"] = 3  # Временное значение для теста
    context.user_data["refresh_limit"] = 3  # Лимит обновлений
    context.user_data["refresh_count"] = 0  # Использованные обновления

    print(
        f"Новый пользователь: {user.first_name} (ID: {user.id}, Username: {user.username})"
    )

    await update.message.reply_text(
        strings.get_welcome_message(context.user_data),
        reply_markup=get_main_menu_keyboard(context.user_data),
        parse_mode="HTML",
    )


async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    callback = query.data

    command = CALLBACK_COMMANDS.get(callback)

    if command:
        await command(update, context)
    #TODO: Добавить обработку на случай несуществующей команды


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
