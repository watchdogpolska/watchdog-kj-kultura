# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-29 22:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_auto_20170127_1215'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metacategory',
            name='user',
        ),
    ]
