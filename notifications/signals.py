import telegram

from notifications.common import send_customer_message, send_kitchen_message, send_courier_message
from notifications.common import render_html_message


def send_order_status_to_customer(order):
    chat = order.user.chat_id
    send_customer_message(chat,         
        render_html_message(
            template="order_status_customer.html",
            order=order,
        ),)

def send_order_to_customer(order):
    chat = order.user.chat_id
    send_customer_message(chat,         
        render_html_message(
            template="order_to_customer.html",
            order=order,
        ),)


def send_order_status_to_kitchen(order):
    send_kitchen_message(         
        render_html_message(
            template="order_status_kitchen.html",
            order=order,
        ),)


def send_new_order_to_kitchen(order):
    send_kitchen_message(         
        render_html_message(
            template="order_status_kitchen.html",
            order=order,
        ),
        reply_markup=telegram.InlineKeyboardMarkup([
                [
                    telegram.InlineKeyboardButton("❌ Отказать", callback_data=f"cancel_order:{order.id}"),
                    telegram.InlineKeyboardButton("🌭 Готовить", callback_data=f"accept_order:{order.id}"),
                ],
            ])
        )


def send_order_status_to_courier(order):
    chat = get_courier_id
    send_courier_message(chat,         
        render_html_message(
            template="order_status_courier.html",
            order=order,
        ),)



# ToDo 

# 4. kitchen states invoice!!
# 4. User Hash
# 5. Nice views
# 7. Check exceptions
# 8. More buttons
# 9. Add map

# ^ it's skeleton for business logic
# next step -- business logic based on telegram messages
# next step -- frontend views for customer and kitchen