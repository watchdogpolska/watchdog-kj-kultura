# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-27 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0002_auto_20170127_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Name'),
        ),
    ]
