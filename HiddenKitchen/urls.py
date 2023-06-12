"""
URL configuration for HiddenKitchen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from customer_bot.views import menu, make_order

def test(request):
    return "Hello world!"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test/', test),
    path('menu.html', menu),
    path('customer/makeOrder', make_order)
]


# https://github.com/mcpeblocker/durgerking-clone-bot/tree/master
# https://github.com/telegram-bot-php/durger-king/tree/master/public
# https://github.com/felixjimcal/telegram_car_dealer_demo
# https://github.com/pashtonchik/sneackers-shop-in-telegram/blob/main/handlers/users/check_profile_info.py
# https://github.com/fruitourist/liot