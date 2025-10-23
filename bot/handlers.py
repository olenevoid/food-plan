from telegram import Update
from telegram.ext import ContextTypes
from .keyboards import get_main_menu_keyboard
from .callbacks import Callback
import bot.strings as strings
import bot.commands as commands


CALLBACK_COMMANDS = {
    Callback.SHOW_RECIPE: commands.show_recipe,
    Callback.OPTION2: commands.show_option2,
    Callback.HELP: commands.show_help,
    Callback.BACK_TO_MENU: commands.back_to_menu,
}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        strings.WELCOME_MESSAGE,
        reply_markup=get_main_menu_keyboard(),
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
