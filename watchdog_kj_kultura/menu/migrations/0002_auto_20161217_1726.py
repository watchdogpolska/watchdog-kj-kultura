# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import watchdog_kj_kultura.menu.validators


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='element',
            name='level',
        ),
        migrations.RemoveField(
            model_name='element',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='element',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='element',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='element',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.Element', verbose_name='Parent'),
        ),
        migrations.AlterField(
            model_name='element',
            name='url',
            field=models.CharField(max_length=100, validators=[watchdog_kj_kultura.menu.validators.is_external_or_valid_url], verbose_name='URL'),
        ),
    ]
