# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-07 09:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='activation_key',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
