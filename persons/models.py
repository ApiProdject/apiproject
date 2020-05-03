from django.db import models

class Person(models.Model):
    name = models.CharField(verbose_name='Name', max_length=64)
    surname = models.CharField(verbose_name='Surname', max_length=64, null=True)