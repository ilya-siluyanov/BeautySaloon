from django.db import models
from django.db.models import fields

from . import Client


class Order(models.Model):
    order_id = fields.AutoField(primary_key=True)
    client = models.ForeignKey(related_name='orders', to=Client, on_delete=models.CASCADE)
    is_complete = fields.BooleanField(default=False)
    pass