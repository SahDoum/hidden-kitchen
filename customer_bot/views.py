from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
import json

from orders.models import Order, MenuItem
from users.models import User

from HiddenKitchen.settings import PROVIDER_TOKEN, CUSTOMER_BOT_TOKEN, APP_SERVER
import customer_bot.handlers
from customer_bot.handlers import bot
from common.security import is_valid_data


def menu(request):
    #user_id = request.GET['user_id']
    user_id = 0
    
    if user_id == None:
        return HttpResponse("Bad Request", status=400)
    # return render(request, "menu.html")
    return render(request, "cafe.html", {
        "menu_items": MenuItem.objects.all(),
        "user_id": user_id,
    })


def create_order_cash(request):
    pass

    # get info from request
    # get user from request
    # get items with request
    # get price
    # validate price
    info = ""
    Order.create_from_telegram(info, cash_payment=True)
    return HttpResponse(json.dumps({"desc":"fine"}), content_type="application/json")


def get_user_info(request):
    # delivery info
    # adresses
    # phone
    # name
    return HttpResponse(json.dumps({"user":"whole info"}), content_type="application/json")


def create_order_from_request(request):
    data = request.POST
    print(data)

    init_data_hash = data.get('initDataHash', 0)
    data_check_string = data.get('dataCheckString', 0)

    user_id = data['user_id']
    user_hash = data['user_hash']
    price = data.get('price', -1)

    user = User.get_telegram_user(user_id, user_hash)
    order = Order.create_from_telegram(user, items=data['order_data'], comment=data['comment'], price=price)

    return order


def create_invoice(request):
    try:
        order = create_order_from_request(request)
    except Exception as ex:
        print(f"Error occurs: {ex}")
        return HttpResponseBadRequest("Error")

    if description == None or payload == None or prices == None:
        return HttpResponse("Bad Request", status=400)

    invoice = bot.createInvoiceLink(
        title="Заказ их Хидден",
        description="Еда, которая насытит тело и дух",
        payload= "hidden-bot-payment",
        provider_token=PROVIDER_TOKEN,
        currency='GEL',
        prices=order.pricesSequence(),
        photo_url= f'{APP_SERVER}/static/img/menu.png',
    )

    return HttpResponse(invoice)


def make_order(request):
    try:
        order = create_order_from_request(request)
    except Exception as ex:
        print(f"Error occurs: {ex}")
        return HttpResponseBadRequest("Error")

    return HttpResponse(json.dumps({"ok":True}), content_type="application/json")
