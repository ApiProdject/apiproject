from django.db import models

class Event(models.Model):
    name = models.CharField(verbose_name='Name', max_length=512)