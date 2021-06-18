from django.db import models
from django.db.models import fields


class Worker(models.Model):
    worker_id = fields.AutoField(primary_key=True)
    name = fields.CharField(max_length=50)
    surname = fields.CharField(max_length=50)
