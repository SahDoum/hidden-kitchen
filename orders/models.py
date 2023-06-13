from django.db import models
from uuid import uuid4

from django.utils.translation import gettext_lazy as _

# from django.contrib.postgres.fields import ArrayField

import notifications.signals as signals

from users.models import User



class Order(models.Model):

    class Statuses(models.TextChoices):
        WAIT = "WT", _("Ждем ответ от Hidden Kitchen")
        ACCEPTED = "AC", _("Ваш заказ готовится")
        READY = "RD", _("Ваш заказ готов и ждет курьера")
        DELIVERY = "DL", _("Ваш заказ будет доставлен в течение X минут")
        DONE = "DN", _("Заказ доставлен")
        ERROR = "ER", _("Произошла ошибка")
        CANCELED = "CL", _("Заказ отменен")

    OS_WAIT     = "wt"
    OS_ACCEPTED = "ac"
    OS_READY    = "rd"
    OS_DELIVERY = "dl"
    OS_DONE     = "dn"
    OS_ERROR    = "er"

    STATUSES = [
        (OS_WAIT, "ждем ответ от Hidden Kitchen"),
        (OS_ACCEPTED, "ваш заказ принят"),
        (OS_READY, "ваш заказ готов и ждет курьера"),
        (OS_DELIVERY, "ваш заказ будет доставлен в течение X минут"),
        (OS_DONE, "заказ доставлен"),
        (OS_ERROR, "произошла ошибка"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Statuses.choices, default=OS_WAIT)

    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    user_cash = models.DecimalField(max_digits=7, decimal_places=2, default=True)
    # items = models.ManyToManyField('MenuItem', related_name='order', blank=True)
    items = models.JSONField(blank=False)

    comment = models.CharField(max_length=200, blank=True)
    review = models.CharField(max_length=200, blank=True)
    err_msg = models.CharField(max_length=200, blank=True)

    @classmethod
    def create_order(cls, user, menu_items, comment=None, user_cash=None):
        # Order.objects.create();
        pass

    def accept(self):
        selt.status = OS_ACCEPTED

    def ready(self):
        selt.status = OS_READY
        # send notification to currier
        # send notification to user

    def delivery(self):
        selt.status = OS_READY
        # send notification to user

    def done(self):
        selt.status = OS_DONE
        # send notification to user

    def error(self, err_msg):
        self.status = OS_ERROR
        self.err_msg = err_msg
        # send notification to user
        # send notification to kitchen?

    @classmethod
    def create_from_telegram(cls, user, items=[], price=-1, comment=None):
        # check menu with price
        order = cls.objects.create(user=user, items=items, comment=comment, price=price)
        signals.send_order_status_to_customer(order)
        return order


    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'


class MenuItem(models.Model):
    code = models.CharField(primary_key=True, max_length=32, null=False, unique=True)

    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.URLField(null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


# https://github.com/legionscript/deliver/tree/tutorial7

