from django.contrib import admin

from orders.models import Order, MenuItem


admin.site.register(Order)
admin.site.register(MenuItem)
