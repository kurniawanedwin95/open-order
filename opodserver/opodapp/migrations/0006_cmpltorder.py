# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-11 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opodapp', '0005_delete_cmpltorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='CmpltOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nama_Order', models.CharField(max_length=100)),
                ('Nomor_PO', models.CharField(max_length=100)),
                ('Item_desc', models.CharField(max_length=100)),
                ('U_of_m', models.CharField(max_length=10)),
                ('Qty', models.CharField(max_length=100)),
                ('Keterangan', models.CharField(max_length=100)),
                ('Tggl_Pengiriman', models.DateField()),
                ('Mesin', models.CharField(max_length=10)),
            ],
        ),
    ]
