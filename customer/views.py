from django.shortcuts import render
from django.http import HttpResponse
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from HiddenKitchen.config import TELEGRAM_BOT_TOKEN


def start_command(update: Update, context: CallbackContext):
    user = update.effective_user
    context.bot.send_message(chat_id=user.id, text="Welcome to the bot app!")


def init_bot():
    # bot = Bot(token=TELEGRAM_BOT_TOKEN)
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    updater.start_polling()
