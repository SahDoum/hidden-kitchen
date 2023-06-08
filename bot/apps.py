from django.apps import AppConfig
from .views import init_bot


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        init_bot()
        