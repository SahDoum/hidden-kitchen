from django.shortcuts import render
from django.http import HttpResponse
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from HiddenKitchen.config import TELEGRAM_BOT_TOKEN

from bot.handlers import start_command, menu_command, unknown_command


def init_bot():
    # bot = Bot(token=TELEGRAM_BOT_TOKEN)
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    updater.start_polling()



# https://github.com/mcpeblocker/durgerking-clone-bot/tree/master
# https://github.com/telegram-bot-php/durger-king/tree/master/public