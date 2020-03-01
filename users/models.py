from django.db import models

class User(models.Model):
    login = models.CharField(verbose_name='Login', max_length=64)
    password = models.CharField(verbose_name='Password', max_length=64)
    USER_LEVELS = (
        (1, 'Admin'),
        (2, 'Simple'),
        (3, 'Extended')
    )
    user_level = models.IntegerField(verbose_name='Level', choices=USER_LEVELS)