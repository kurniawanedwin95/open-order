# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-17 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opodapp', '0014_delete_cmpltorder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='production',
            old_name='Item_Desc',
            new_name='Item_desc',
        ),
        migrations.AlterField(
            model_name='production',
            name='Tggl_Mulai_Produksi',
            field=models.CharField(max_length=100),
        ),
    ]
