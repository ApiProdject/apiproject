from django.db import models

from emotionTypes.models import EmotionTypes
from persons.models import Person

# Create your models here.
from stands.models import Stand


class Match(models.Model):
    personId = models.ForeignKey(Person, verbose_name='personID', on_delete=models.CASCADE)
    standID = models.ForeignKey(Stand, verbose_name='standID', on_delete=models.CASCADE)
    emotionId = models.ForeignKey(EmotionTypes, verbose_name='emotionID', on_delete=models.CASCADE, null=True)