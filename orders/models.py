from django.db import models
from uuid import uuid4
# from django.contrib.postgres.fields import ArrayField


from users.models import User



class Order(models.Model):

    STATUS1 = "status1"
    STATUS2 = "status2"
    STATUS3 = "status3"

    STATUSES = [
        (STATUS1, "status1"),
        (STATUS2, "status2"),
        (STATUS3, "status3"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # status = ArrayField(models.CharField(max_length=32, choices=STATUSES), default=list, null=False)

    # menu list
    # status
