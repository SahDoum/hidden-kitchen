from notifications.common import send_customer_message, send_kitchen_message, send_courier_message
from notifications.common import render_html_message


def send_order_status_to_customer(order):
    chat = order.user.chat_id
    send_customer_message(chat,         
        render_html_message(
            template="order_status_customer.html",
            order=order,
        ),)


def send_order_status_to_kitchen(order):
    chat = KITCHEN_ID
    send_kitchen_message(chat,         
        render_html_message(
            template="order_status_kitchen.html",
            order=order,
        ),)


def send_order_status_to_courier(order):
    chat = get_courier_id
    send_courier_message(chat,         
        render_html_message(
            template="order_status_courier.html",
            order=order,
        ),)



# ToDo 
# 1. menu from file
# 2. menu field in order
# 3. 3 bots, 3 types signals
# 4. notifications with buttons

# ^ it's skeleton for business logic
# next step -- business logic based on telegram messages
# next step -- frontend views for customer and kitchen