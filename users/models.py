from django.db import models
from uuid import uuid4


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    telegram_id = models.UUIDField(default=uuid4)

    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    # Add other fields as needed


class Adress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    adress = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    # Add other fields as needed
