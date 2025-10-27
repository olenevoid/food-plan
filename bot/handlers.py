from telegram import Update
from telegram.ext import ContextTypes
from .callbacks import Callback
import bot.commands as commands
from asgiref.sync import sync_to_async
from food_plan_app import db_requests as db


CALLBACK_COMMANDS = {
    Callback.SHOW_RECIPE: commands.show_recipe,
    Callback.BACK_TO_MENU: commands.back_to_menu,
    Callback.ANOTHER_RECIPE: commands.another_recipe,
    Callback.CLEAR_BLACKLIST: commands.clear_blacklist,
    Callback.LIKE_RECIPE: commands.like_recipe,
    Callback.DISLIKE_RECIPE: commands.dislike_recipe,
}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    user = await sync_to_async(db.find_serialized_user_by_tg_id)(chat_id)
    if not user:
        tg_user = update.effective_user
        await sync_to_async(db.add_user)(chat_id, tg_user.first_name)
        user = await sync_to_async(db.find_serialized_user_by_tg_id)(chat_id)

    if "message_history" in context.user_data:
        context.user_data["message_history"] = []

    await commands.show_main_menu(update, context)


async def handle_button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    callback = query.data

    command = CALLBACK_COMMANDS.get(callback)

    if command:
        await command(update, context)
    # TODO: Добавить обработку на случай несуществующей команды


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
