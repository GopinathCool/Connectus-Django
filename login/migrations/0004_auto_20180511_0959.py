# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-11 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='audio',
            field=models.FilePathField(default=django.utils.timezone.now, path='/home/dev/connectus/media/uploads/testupload/testforms.py'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=b''),
        ),
    ]
