from django.db import models

from django.db import models

from emotionTypes.models import EmotionTypes
from stands.models import Stand


class InfoPoint(models.Model):
    standId = models.ForeignKey(Stand, verbose_name='standID', on_delete=models.CASCADE)
    emotionTypeID = models.ForeignKey(EmotionTypes, verbose_name='emotionID', on_delete=models.CASCADE, null=True)
    age = models.IntegerField(verbose_name='age', null=True)
    SEXES = (
        (1, 'Male'),
        (2, 'Female')
    )
    sex = models.IntegerField(verbose_name='sex', choices=SEXES, null=True)
