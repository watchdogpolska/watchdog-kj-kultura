# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-12 05:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations_requests', '0002_auto_20161212_0542'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='introduction',
            field=models.TextField(blank=True, verbose_name='Introduction'),
        ),
    ]
