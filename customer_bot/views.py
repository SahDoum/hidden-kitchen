from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

import json

from orders.models import Order, MenuItem
from users.models import User


from HiddenKitchen.settings import PROVIDER_TOKEN
import customer_bot.handlers


def menu(request):
    # return render(request, "menu.html")
	return render(request, "cafe.html", {"menu_items": MenuItem.objects.all()})


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


def create_order_invoice(request):
    # just invoice and handler for invoice success? 
    # Or order with status "wait payment"?
    # how to accept invoice receipt?
    pass


def get_user_info(request):
    # delivery info
    # adresses
    # phone
    # name
    return HttpResponse(json.dumps({"user":"whole info"}), content_type="application/json")


def make_order(request):
    # init_data_hash = request.GET['initDataHash']
    # data_check_string = request.GET['dataCheckString']
    
    # # if not is_valid_data(init_data_hash, data_check_string):
    # #     return HttpResponse("Unauthorized", status=401)


    # description = request.GET['description']
    # payload = request.GET['payload']
    # prices = request.GET['prices']

    # if description == None or payload == None or prices == None:
    #     return HttpResponse("Bad Request", status=400)

    # response = requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/createInvoiceLink', {
    #     'title': "Запись",
    #     'description': description,
    #     'payload': payload,
    #     'provider_token': PROVIDER_TOKEN,
    #     'currency': 'GEL',
    #     'prices': prices,
    #     'photo_url': 'https://user-images.githubusercontent.com/70770455/195734898-ac0a1171-be48-4773-b382-7f6430df9744.png',
    #     'need_name': True,
    #     'need_phone_number': False,
    #     }
    # )
    print("Making order")
    print(request)
    print(request.method)
    print(request.POST)
    data = request.POST
    user_id = data['user_id']
    user_hash = data['user_hash']
    price = data.get('price', -1)

    print(data['order_data'])
    print(user_id)

    try:
        user = User.get_telegram_user(user_id, user_hash)
    except User.DoesNotExist:
        print("Error. User Does Not Exist")
        return HttpResponseBadRequest("User does not exists")


    order = Order.create_from_telegram(user, items=data['order_data'], comment=data['comment'], price=price)
    return HttpResponse(json.dumps({"ok":True}), content_type="application/json")
