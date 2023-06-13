from django.template import loader

import telegram
from telegram import ParseMode
from notifications.bot import customer_bot, kitchen_bot, courier_bot



def render_html_message(template, **data):
    tmpl = loader.get_template(template)
    return tmpl.render({
        **data,
        # "settings": settings
    })


def send_telegram_message(
    bot,
    chat_id: int,
    text: str,
    parse_mode: ParseMode = telegram.ParseMode.HTML,
    disable_preview: bool = True,
    **kwargs
):
    try:
        return bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_preview,
            **kwargs
        )
    except telegram.error.TelegramError as ex:
        log.warning(f"Telegram error: {ex}")


def send_customer_message(
    chat_id: int,
    text: str,
    parse_mode: ParseMode = telegram.ParseMode.HTML,
    disable_preview: bool = True,
    **kwargs
):
    send_telegram_message(
        customer_bot,
        chat_id,
        text,
        parse_mode,
        disable_preview,
        **kwargs
        )

def send_kitchen_message():
    pass

def send_courier_message():
    pass

