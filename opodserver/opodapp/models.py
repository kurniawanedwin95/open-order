# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Order(models.Model):
    Nomor_PO = models.CharField(max_length = 100)
    Item_desc = models.CharField(max_length = 100)
    U_of_m = models.CharField(max_length = 10)
    Qty = models.CharField(max_length = 100)
    Keterangan = models.CharField(max_length = 100)
    Tggl_Pengiriman = models.DateField()

class CmpltOrder(models.Model):
    Nomor_PO = models.CharField(max_length = 100)
    Item_desc = models.CharField(max_length = 100)
    U_of_m = models.CharField(max_length = 10)
    Qty = models.CharField(max_length = 100)
    Keterangan = models.CharField(max_length = 100)
    Tggl_Pengiriman = models.DateField()
    Mesin = models.CharField(max_length = 10)
  
