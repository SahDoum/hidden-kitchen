from django.apps import AppConfig
from .views import init_bot


class CustomerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer'

    def ready(self):
        init_bot()
