from django.http import HttpResponse
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ContextTypes, Filters, PreCheckoutQueryHandler

from users.models import User

from HiddenKitchen.settings import CUSTOMER_BOT_TOKEN, APP_SERVER


def start_command(update: Update, context: CallbackContext) -> None:
    tgUser = update.effective_user
    user = User.create_from_telegram(tgUser)

    # inline_keyboard_markup = InlineKeyboardMarkup(inline_keyboard=[
    #     [InlineKeyboardButton("Меню", web_app=WebAppInfo(url=f'{APP_SERVER}/menu?user_id={user.id}'))],
    # ])

    context.bot.send_message(chat_id=tgUser.id, text="Добро пожаловать в HiddenKitchen!", reply_markup=inline_keyboard_markup)


def successful_payment_callback(update: Update) -> None:
    """Confirms the successful payment."""
    # do something after successfully receiving payment?
    payment = update.message.successful_payment

    print(payment)
    print(payment.invoice_payload)
    print(payment.order_info)
    print(payment.telegram_payment_charge_id)
    print(payment.provider_payment_charge_id)

    # get order, update status

    update.message.reply_text("Thank you for your payment!")


def precheckout_callback(update: Update, _: CallbackContext) -> None:
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'hidden-bot-payment':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
    else:
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

init_polling()
