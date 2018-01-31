# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-31 17:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opodapp', '0025_auto_20180116_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmpltorder',
            name='Tggl_Masuk_Order',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='Tggl_Order_Masuk',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='production',
            name='Tggl_Order_Masuk',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cmpltorder',
            name='Item_desc',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='order',
            name='Item_desc',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='production',
            name='Item_desc',
            field=models.CharField(max_length=300),
        ),
        migrations.RunSQL(
            "UPDATE opodapp_sortedcustomerlist SET Sorted_Customer_Number='ZZ9999' WHERE Sorted_Customer_Name='Lihat item desc';"
        ),
    ]
