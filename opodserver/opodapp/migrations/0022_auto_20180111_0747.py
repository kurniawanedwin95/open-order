# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-11 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opodapp', '0021_auto_20180109_1502'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cmpltorder',
            name='Product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='Product',
        ),
        migrations.RemoveField(
            model_name='production',
            name='Product',
        ),
        migrations.AddField(
            model_name='cmpltorder',
            name='Product_Name',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='Product_Name',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='production',
            name='Product_Name',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
