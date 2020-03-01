# Generated by Django 3.0.3 on 2020-02-26 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=64, verbose_name='Login')),
                ('password', models.CharField(max_length=64, verbose_name='Password')),
                ('user_level', models.IntegerField(choices=[(1, 'Admin'), (2, 'Simple'), (3, 'Extended')], verbose_name='Level')),
            ],
        ),
    ]
