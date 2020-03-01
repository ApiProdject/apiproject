from django.db import models
from persons.models import Person

# Create your models here.
class Photo(models.Model):
    address = models.CharField(verbose_name='address', max_length=512)
    personId = models.ForeignKey(Person, verbose_name='personID', on_delete=models.CASCADE)
