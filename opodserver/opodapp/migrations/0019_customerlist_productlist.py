# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-08 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opodapp', '0018_auto_20171219_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer_Name', models.CharField(max_length=100)),
                ('Customer_Address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ProductList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_Name', models.CharField(max_length=50)),
                ('Product_Thickness', models.CharField(max_length=10)),
            ],
        ),
    ]