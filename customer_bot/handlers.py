from django.http import HttpResponse
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from users.models import User
from updater import updater


def start_command(update: Update, context: CallbackContext):
    user = update.effective_user
    User.create_from_telegram(user)
    context.bot.send_message(chat_id=user.id, text="Welcome to the bot app!")


def menu(request):
    return render(request, "menu.html")
