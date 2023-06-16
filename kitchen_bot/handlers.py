from django.http import HttpResponse
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler

from users.models import User
from orders.models import Order

from telegram.ext import Updater
from HiddenKitchen.settings import KITCHEN_BOT_TOKEN, KITCHEN_ID


def start_command(update: Update, context: CallbackContext):
    tgUser = update.effective_user
    user = User.create_from_telegram(tgUser)
    print("New user:")
    print(tgUser)
    context.bot.send_message(chat_id=tgUser.id, text="Welcome to the bot app!")


def set_kitchen(update: Update, context: CallbackContext):
    KITCHEN_ID = update.effective_user.id
    context.bot.send_message(chat_id=KITCHEN_ID, text="Update Id")


def cancel_order(update: Update, context: CallbackContext):
    _, order_id = update.callback_query.data.split(":", 1)
    order = Order.objects.get(id=order_id)
    if order.status == Order.Statuses.CANCELED:
        update.effective_chat.send_message(
            f"Заказ «{order.id}» уже был отклонен"
        )
        update.callback_query.edit_message_reply_markup(reply_markup=None)
        return None

    order.cancel()

    update.effective_chat.send_message(
        f"Заказ «{order.id}» отклонен"
    )
    update.callback_query.edit_message_reply_markup(reply_markup=None)
    return None


def accept_order(update: Update, context: CallbackContext):
    _, order_id = update.callback_query.data.split(":", 1)
    order = Order.objects.get(id=order_id)
    if order.status == Order.Statuses.CANCELED:
        update.effective_chat.send_message(
            f"Заказ «{order.id}» уже был отклонен"
        )
        update.callback_query.edit_message_reply_markup(reply_markup=None)
        return None

    order.cancel()

    update.effective_chat.send_message(
        f"Заказ «{order.id}» отклонен"
    )
    update.callback_query.edit_message_reply_markup(reply_markup=None)
    return None


updater = Updater(token=KITCHEN_BOT_TOKEN, use_context=True)
def init_polling():
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("kitchen", set_kitchen))

    dispatcher.add_handler(CallbackQueryHandler(cancel_order, pattern=r"^cancel_order:.+"))
    dispatcher.add_handler(CallbackQueryHandler(accept_order, pattern=r"^accept_order:.+"))


    print("Starting polling")
    updater.start_polling()

init_polling()
