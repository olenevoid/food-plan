from telegram.ext import Application
from bot.settings import BOT_TOKEN
from bot.handlers import start_command, handle_button_click, error_handler
from telegram.ext import CommandHandler, CallbackQueryHandler


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(handle_button_click))
    
    # Error handler
    #app.add_error_handler(error_handler)

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
