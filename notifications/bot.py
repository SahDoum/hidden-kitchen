import telegram
from django.conf import settings

customer_bot = telegram.Bot(token=settings.CUSTOMER_BOT_TOKEN) if settings.CUSTOMER_BOT_TOKEN else None
kitchen_bot = telegram.Bot(token=settings.KITCHEN_BOT_TOKEN) if settings.KITCHEN_BOT_TOKEN else None
courier_bot = telegram.Bot(token=settings.COURIER_BOT_TOKEN) if settings.COURIER_BOT_TOKEN else None
