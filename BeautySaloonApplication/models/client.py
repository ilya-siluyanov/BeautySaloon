from django.db import models
from django.db.models import fields


class Client(models.Model):
    phone_number = fields.CharField(primary_key=True, max_length=12)
    name = fields.CharField(max_length=50)
    surname = fields.CharField(max_length=50)
