from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import get_main_menu_keyboard
from .callbacks import Callback
import bot.strings as strings
import bot.commands as commands
from asgiref.sync import sync_to_async
from food_plan_app import db_requests as db


CALLBACK_COMMANDS = {
    Callback.SHOW_RECIPE: commands.show_recipe,
    Callback.BACK_TO_MENU: commands.back_to_menu,
    Callback.ANOTHER_RECIPE: commands.another_recipe,
    Callback.CLEAR_BLACKLIST: commands.clear_blacklist,
}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    chat_id = '55555555555' #update.effective_chat.id

    user = await sync_to_async(db.find_user_by_tg_id)(chat_id)
    if not user:
        tg_user = update.effective_user
        #TODO: Создаем нового пользователя на сервере

    await update.message.reply_text(
        strings.get_welcome_message(user),
        reply_markup=get_main_menu_keyboard(user),
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
