from telegram import Update
from telegram.ext import CallbackContext


def start_command(update: Update, context: CallbackContext):
    user = update.effective_user
    context.bot.send_message(chat_id=user.id, text="Welcome to the bot app!")


def menu_command(update: Update, context: CallbackContext):
    user = update.effective_user
    menu_items = MenuItem.objects.all()
    message = "Menu:\n"
    for item in menu_items:
        message += f"- {item.name}: ${item.price}\n"
    context.bot.send_message(chat_id=user.id, text=message)


def unknown_command(update: Update, context: CallbackContext):
    user = update.effective_user
    context.bot.send_message(chat_id=user.id, text="Sorry, I don't understand that command.")

