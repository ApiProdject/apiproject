from django.db import models
from users.models import User
from stands.models import Stand

# Create your models here.
class UserStand(models.Model):
    owner = models.ForeignKey(User, verbose_name='owner', max_length=512, on_delete=models.CASCADE)
    standId = models.ForeignKey(Stand, verbose_name='stand', max_length=512, on_delete=models.CASCADE)