# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 01:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('PepBandWebsite', '0018_auto_20170720_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='eboard',
            name='slug',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
