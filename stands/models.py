from django.db import models
from events.models import Event

class Stand(models.Model):
    eventId = models.ForeignKey(Event, verbose_name='eventId', max_length=512, on_delete=models.CASCADE)
    person = models.BooleanField(verbose_name='person')
    emotion = models.BooleanField(verbose_name='emotion')
    age = models.BooleanField(verbose_name='age')
    sex = models.BooleanField(verbose_name='sex')
    people = models.BooleanField(verbose_name='people')
