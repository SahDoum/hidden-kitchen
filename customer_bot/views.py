from django.shortcuts import render
from django.http import HttpResponse

import json

from HiddenKitchen.settings import TELEGRAM_BOT_TOKEN, PROVIDER_TOKEN


def menu(request):
	return render(request, "menu.html")


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
    return HttpResponse(json.dumps({"desc":"fine"}), content_type="application/json")
