# Generated by Django 3.1.4 on 2021-02-04 12:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='default_phone_number',
            field=models.CharField(blank=True, max_length=8, null=True, validators=[django.core.validators.RegexValidator('^\\d{8}$', message='Incorrect number format')]),
        ),
    ]