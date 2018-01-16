# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-16 11:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opodapp', '0024_sortedcustomerlist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cmpltorder',
            old_name='Customer_Number',
            new_name='Customer_Name',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='Customer_Number',
            new_name='Customer_Name',
        ),
        migrations.RenameField(
            model_name='production',
            old_name='Customer_Number',
            new_name='Customer_Name',
        ),
        migrations.RunSQL(
            "INSERT INTO opodapp_sortedcustomerlist (Sorted_Customer_Name, Sorted_Customer_Number) VALUES ('Lihat item desc', 'EXTRA');"
        ),
    ]