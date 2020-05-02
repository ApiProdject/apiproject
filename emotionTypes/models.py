from django.db import models


class EmotionTypes(models.Model):
    name = models.CharField(verbose_name='Name', max_length=512)
    emotion_number = models.IntegerField(verbose_name='emotion_number')
