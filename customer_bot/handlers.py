from django.http import HttpResponse
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ContextTypes, Filters, PreCheckoutQueryHandler

from users.models import User
from orders.models import Order

from HiddenKitchen.settings import CUSTOMER_BOT_TOKEN, APP_SERVER
import uuid



def start_command(update: Update, context: CallbackContext) -> None:
    tgUser = update.effective_user
    user = User.create_from_telegram(tgUser)

    context.bot.send_message(chat_id=tgUser.id, text="Добро пожаловать в HiddenKitchen!")


def successful_payment_callback(update: Update, _) -> None:
    payment = update.message.successful_payment

    code, uid_str = payment.invoice_payload.split('@', 1)

    if code != 'hpb':
        update.message.reply_text("Что-то пошло не так...")
        return

    # get order, update status

    uid = uuid.UUID(uid_str)
    order = Order.objects.get(id=uid)
    order.paid()

    update.message.reply_text("Ваша оплата прошла, ждем ответа от кухни!")


def precheckout_callback(update: Update, _: CallbackContext) -> None:
    query = update.pre_checkout_query
    code, uid_str = query.invoice_payload.split('@', 1)
    # check the payload, is this from your bot?
    if code != 'hpb':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Что-то пошло не так...")

    uid = uuid.UUID(uid_str)
    order = Order.objects.get(id=uid)
    query.answer(ok=True)


bot = Bot(token=CUSTOMER_BOT_TOKEN) # should I move it to notifications?
updater = Updater(token=CUSTOMER_BOT_TOKEN, use_context=True)
def init_polling():
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(
        MessageHandler(Filters.successful_payment, successful_payment_callback)
    )
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))


    print("Starting polling")
    updater.start_polling()
