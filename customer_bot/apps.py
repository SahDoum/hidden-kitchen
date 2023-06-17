from django.apps import AppConfig
import sys
import os



class CustomerBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_bot'

    def ready(self):
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN'):
            from customer_bot.handlers import init_polling
            init_polling()
