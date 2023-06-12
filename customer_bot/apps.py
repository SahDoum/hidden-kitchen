from django.apps import AppConfig
from customer_bot.handlers import init_bot


class CustomerBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer_bot'

    def ready(self):
        # return
        init_bot()
