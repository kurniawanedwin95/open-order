# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-19 10:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opodapp', '0016_cmpltorder'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmpltorder',
            name='Output',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
