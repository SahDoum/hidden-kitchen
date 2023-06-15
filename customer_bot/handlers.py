from django.http import HttpResponse
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from users.models import User

from telegram.ext import Updater
from HiddenKitchen.settings import CUSTOMER_BOT_TOKEN


def start_command(update: Update, context: CallbackContext):
    tgUser = update.effective_user
    user = User.create_from_telegram(tgUser)
    print("New user:")
    print(tgUser)
    context.bot.send_message(chat_id=tgUser.id, text="Welcome to the bot app!")


def menu(request):
    return render(request, "menu.html")


updater = Updater(token=CUSTOMER_BOT_TOKEN, use_context=True)
def init_polling():
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))

    print("Starting polling")
    updater.start_polling()

init_polling()
