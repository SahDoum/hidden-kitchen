import hmac
from hashlib import sha256
from urllib.parse import unquote
from orders.models import Order, MenuItem
from users.models import User

from HiddenKitchen.settings import CUSTOMER_BOT_TOKEN


secret_key = hmac.new(b'WebAppData', bytes(CUSTOMER_BOT_TOKEN, encoding='utf-8'), sha256).digest()


def is_valid_data(init_data_hash: str, data_check_string: str) -> bool:
    data_check_string_unquote = unquote(data_check_string.replace('&', '\n'))

    hash = hmac.new(secret_key, bytes(data_check_string_unquote, encoding='utf-8'), sha256).hexdigest()

    if hash == init_data_hash:
        return True
    else:
        return False


def create_order_from_request(request):
    data = request.POST

    init_data_hash = data.get('initDataHash', 0)
    data_check_string = data.get('dataCheckString', 0)

    user_id = data.get('user_id', 0)
    user_hash = data.get('user_hash', 0)
    price = data.get('price', -1)

    print("Request data:")
    print(init_data_hash)
    print(data_check_string)
    print(user_id)
    print(user_hash)

    is_inside = True
    is_cash_payment = True
    user_cash = -1

    user = User.get_telegram_user(user_id, user_hash)
    order = Order.create_from_telegram(
        user, 
        items=json.loads(data['order_data']), 
        is_inside=is_inside,
        is_cash_payment=is_cash_payment,
        price=price,
        user_cash=user_cash,
        comment=data['comment'], 
    )
    order.pricesSequence()

    return order