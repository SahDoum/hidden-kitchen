from django.http import HttpResponse
from telegram import Update
import telegram
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler

from users.models import User
from orders.models import Order

from telegram.ext import Updater
from HiddenKitchen.settings import KITCHEN_BOT_TOKEN, KITCHEN_ID
from notifications.common import render_html_message
from telegram import ParseMode



def start_command(update: Update, context: CallbackContext):
    tgUser = update.effective_user
    user = User.create_from_telegram(tgUser)
    print("New user:")
    print(tgUser)
    context.bot.send_message(chat_id=tgUser.id, text="Welcome to the bot app!")


def set_kitchen(update: Update, context: CallbackContext):
    global KITCHEN_ID
    KITCHEN_ID = update.effective_user.id
    context.bot.send_message(chat_id=KITCHEN_ID, text="Update Id")


def cancel_order(update: Update, context: CallbackContext):
    _, order_id = update.callback_query.data.split(":", 1)

    order = Order.objects.get(id=order_id)
    order.cancel()

    update.callback_query.edit_message_text(   
        render_html_message(
            template="order_status_kitchen.html",
            order=order,
        ),
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )
    return None


def accept_order(update: Update, context: CallbackContext):
    _, order_id = update.callback_query.data.split(":", 1)
    order = Order.objects.get(id=order_id)
    # Add checks later
    order.accept()

    update.callback_query.edit_message_text(   
        render_html_message(
            template="order_status_kitchen.html",
            order=order
        ),
        reply_markup=telegram.InlineKeyboardMarkup([
            [
                telegram.InlineKeyboardButton("🏃‍♀️ Отправить с курьером", callback_data=f"delivery_order:{order.id}"),
            ],
        ]),
        parse_mode=ParseMode.HTML
    )

    return None


def delivery_order(update: Update, context: CallbackContext):
    _, order_id = update.callback_query.data.split(":", 1)
    order = Order.objects.get(id=order_id)

    order.delivery()
    update.callback_query.edit_message_text(   
        render_html_message(
            template="order_status_kitchen.html",
            order=order,
        ),
        reply_markup=None,
        parse_mode=ParseMode.HTML
    )



updater = Updater(token=KITCHEN_BOT_TOKEN, use_context=True)
def init_polling():
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("kitchen", set_kitchen))

    dispatcher.add_handler(CallbackQueryHandler(cancel_order, pattern=r"^cancel_order:.+"))
    dispatcher.add_handler(CallbackQueryHandler(accept_order, pattern=r"^accept_order:.+"))
    dispatcher.add_handler(CallbackQueryHandler(accept_order, pattern=r"^delivery_order:.+"))


    print("Starting polling")
    updater.start_polling()
