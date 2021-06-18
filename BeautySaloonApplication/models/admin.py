from django.db import models
from django.db.models import fields


class Admin(models.Model):
    admin_id = fields.AutoField(primary_key=True)
    name = fields.CharField(max_length=50, null=False, blank=False)
    surname = fields.CharField(max_length=50, null=False, blank=False)
