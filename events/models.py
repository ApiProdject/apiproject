from django.db import models


class Event(models.Model):
    name = models.CharField(verbose_name='Name', unique=True, max_length=512)
