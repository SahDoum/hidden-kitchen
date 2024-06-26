from django.db import models
from uuid import uuid4
import json

from django.utils.translation import gettext_lazy as _
import notifications.signals as signals

from telegram import LabeledPrice
from users.models import User



class Order(models.Model):

    OS_UNPAID  = "up"
    OS_WAIT     = "wt"
    OS_ACCEPTED = "ac"
    OS_READY    = "rd"
    OS_DELIVERY = "dl"
    OS_DONE     = "dn"
    OS_ERROR    = "er"
    OS_CANCELED = "cl"

    STATUSES = [
        (OS_UNPAID, 'ждем оплаты'),
        (OS_WAIT, "ждем ответ от Hidden Kitchen"),
        (OS_ACCEPTED, "ваш заказ принят"),
        (OS_READY, "ваш заказ готов и ждет курьера"),
        (OS_DELIVERY, "ваш заказ будет доставлен в течение X минут"),
        (OS_DONE, "заказ доставлен"),
        (OS_ERROR, "произошла ошибка"),
        (OS_CANCELED, "отменен"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    pretty_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUSES, default=OS_WAIT)

    items = models.JSONField(blank=False)
    is_inside = models.BooleanField(blank=False)
    is_cash_payment = models.BooleanField(blank=False)
    price = models.IntegerField()
    user_cash = models.IntegerField()

    comment = models.CharField(max_length=200, blank=True)
    review = models.CharField(max_length=200, blank=True)

    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    err_msg = models.CharField(max_length=200, blank=True)


    @classmethod
    def create_from_telegram(cls, user, items, is_inside, is_cash_payment, price=-1, user_cash=-1, comment=None):

        status = OS_WAIT if is_cash_payment else OS_UNPAID
        pretty_id = cls.objects.filter(is_inside=is_inside).count()
        order = cls.objects.create(
            pretty_id=pretty_id%999 + 1,
            user=user, 
            status=status,
            items=items, 
            comment=comment, 
            price=price,
            is_inside=is_inside,
            is_cash_payment=is_cash_payment,
            user_cash=user_cash,
        )

        if is_cash_payment:
            signals.send_order_to_customer(order)
            signals.send_new_order_to_kitchen(order)
        return order

    def pricesSequence(self):
        seq = []
        for code, count in self.items.items():
            item = MenuItem.objects.get(code=code)
            seq.append(LabeledPrice(f'{item.name} x{count}', item.price*count))
        return seq

    @property
    def description(self):
        desc = ''
        for code, count in self.items.items():
            item = MenuItem.objects.get(code=code)
            desc += f'{item.name} x{count}\n'
        return desc

    @property
    def number(self):
        letter = 'A' if self.is_inside else 'B'
        return f'{letter}-{self.pretty_id:03d}'


    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'


    def paid(self):
        if self.status != Order.OS_UNPAID:
            return

        self.status = Order.OS_WAIT
        self.save()

        signals.send_order_to_customer(order)
        signals.send_new_order_to_kitchen(order)


    def accept(self):
        self.status = Order.OS_ACCEPTED
        self.save()
        signals.send_order_status_to_customer(self)

    def delivery(self):
        self.status = Order.OS_DELIVERY
        self.save()
        signals.send_order_status_to_customer(self)

    def cancel(self):
        self.status = Order.OS_CANCELED
        self.save()
        signals.send_order_status_to_customer(self)


class MenuItem(models.Model):
    code = models.CharField(primary_key=True, max_length=32, null=False, unique=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField(null=False)
    price = models.IntegerField()

    def __str__(self):
        return self.name

    @property
    def decimal_price(self):
        return self.price*.01


# https://github.com/legionscript/deliver/tree/tutorial7

