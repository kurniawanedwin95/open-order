# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-31 17:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('opodapp', '0026_auto_20180131_1733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cmpltorder',
            old_name='Tggl_Masuk_Order',
            new_name='Tggl_Order_Masuk',
        ),
    ]
