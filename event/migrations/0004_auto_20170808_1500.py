# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-08 15:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20170805_1919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='venue',
            options={'ordering': ['country', 'city', 'name']},
        ),
    ]