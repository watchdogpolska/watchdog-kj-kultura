# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-27 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20170127_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='jst',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teryt_tree.JednostkaAdministracyjna', verbose_name='Unit of administrative division'),
        ),
    ]
