# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-20 19:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20171120_1401'),
    ]

    operations = [
        migrations.AddField(
            model_name='datagroup',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]