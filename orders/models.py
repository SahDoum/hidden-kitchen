from django.db import models
from uuid import uuid4
# from django.contrib.postgres.fields import ArrayField


from users.models import User



class Order(models.Model):

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
    status = models.CharField(max_length=2, choices=STATUSES, default=OS_WAIT)

    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    user_cash = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('MenuItem', related_name='order', blank=True)

    comment = models.CharField(max_length=200)
    review = models.CharField(max_length=200)
    err_msg = models.CharField(max_length=200)

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




    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # image = models.ImageField(upload_to='menu_images/')
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


# https://github.com/legionscript/deliver/tree/tutorial7

