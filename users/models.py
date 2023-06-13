from django.db import models
from uuid import uuid4


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chat_id = models.IntegerField(unique=True)

    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    # Add other fields as needed

    @classmethod
    def create_from_telegram(cls, user):
        tgUser = cls.get_or_create(chat_id=user.id)
        return tgUser

    @classmethod
    def get_telegram_user(cls, user_id, user_hash):
        # chack hash
        return cls.objects.get(chat_id=user_id)


class Adress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    adress = models.CharField(max_length=200)
    comment = models.CharField(max_length=200)
    # Add other fields as needed
