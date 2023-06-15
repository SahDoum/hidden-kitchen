from django.http import HttpResponse
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from users.models import User
# from updater import updater


from telegram.ext import Updater
from HiddenKitchen.settings import CUSTOMER_BOT_TOKEN


def start_command(update: Update, context: CallbackContext):
    tgUser = update.effective_user
    user = User.create_from_telegram(tgUser)
    print("New user:")
    print(user)
    context.bot.send_message(chat_id=user.id, text="Welcome to the bot app!")


def menu(request):
    return render(request, "menu.html")


# def start_polling():
#     if start_polling.POLLINT_STARTED:
#         return
#     print("POLLING!!!!!!")
#     start_polling.POLLINT_STARTED = True
#     updater = Updater(token=CUSTOMER_BOT_TOKEN, use_context=True)
#     dispatcher = updater.dispatcher
#     dispatcher.add_handler(CommandHandler("start", start_command))
#     updater.start_polling()

# start_polling.POLLINT_STARTED = False
# start_polling()
