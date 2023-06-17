from django.apps import AppConfig
import sys
import os


class KitchenBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kitchen_bot'

    def ready(self):
        if 'runserver' in sys.argv and os.environ.get('RUN_MAIN'):
            from kitchen_bot.handlers import init_polling
            init_polling()