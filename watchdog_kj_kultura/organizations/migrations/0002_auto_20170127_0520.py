# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-27 04:20
from __future__ import unicode_literals

from django.db import migrations, models
import watchdog_kj_kultura.organizations.validators


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial_squashed_0007_auto_20161230_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metacategory',
            name='key',
            field=models.CharField(help_text='They are permitted only Latin characters and numbers.', max_length=50, validators=[watchdog_kj_kultura.organizations.validators.is_allnum], verbose_name='Key'),
        ),
    ]