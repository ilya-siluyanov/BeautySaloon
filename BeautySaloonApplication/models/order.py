from django.db import models
from django.db.models import fields
from django.utils import timezone
from . import Client, Service


class Order(models.Model):
    order_id = fields.AutoField(primary_key=True)
    client = models.ForeignKey(related_name='orders', to=Client, on_delete=models.CASCADE)
    service = models.ForeignKey(related_name='orders', to=Service, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False, default='2000-01-01')
    time = models.TimeField(null=False, blank=False, default='00:00')
    is_complete = fields.BooleanField(default=False)
