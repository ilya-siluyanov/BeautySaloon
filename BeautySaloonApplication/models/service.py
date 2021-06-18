from django.db import models
from django.db.models import fields


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    name = fields.CharField(max_length=255)
    price = fields.IntegerField(default=0)
