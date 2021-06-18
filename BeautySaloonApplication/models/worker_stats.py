from django.db import models
from django.db.models import fields
from . import Worker


class WorkerStats(models.Model):
    stats_id = fields.AutoField(primary_key=True)
    worker = models.OneToOneField(related_name='statistics', to=Worker, on_delete=models.CASCADE)
    rating = fields.FloatField()  # FIXME: add constraint max 5.0
