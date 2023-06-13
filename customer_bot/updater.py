from telegram.ext import Updater

from HiddenKitchen.settings import CUSTOMER_BOT_TOKEN


updater = Updater(token=CUSTOMER_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start_command))
updater.start_polling()