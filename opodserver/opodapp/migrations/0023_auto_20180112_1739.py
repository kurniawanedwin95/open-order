# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-12 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opodapp', '0022_auto_20180111_0747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productlist',
            name='Product_Thickness',
        ),
        migrations.AddField(
            model_name='cmpltorder',
            name='Customer_Number',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='Customer_Number',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='production',
            name='Customer_Number',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cmpltorder',
            name='Product_Name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='Product_Name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='production',
            name='Product_Name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='productlist',
            name='Product_Name',
            field=models.CharField(max_length=100),
        ),
    ]
