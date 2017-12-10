# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Order(models.Model):
    Nama_Order = models.CharField(max_length = 100)
    Nomor_PO = models.CharField(max_length = 30)
    Item_desc = models.CharField(max_length = 100)
    U_of_m = models.CharField(max_length = 10)
    Qty = models.CharField(max_length = 100)
    Keterangan = models.CharField(max_length = 100)
    Tggl_Pengiriman = models.CharField(max_length = 30)
    
class CmpltOrder(models.Model):
    Nama_Order = models.CharField(max_length = 100)
    Nomor_PO = models.CharField(max_length = 30)
    Item_desc = models.CharField(max_length = 100)
    U_of_m = models.CharField(max_length = 10)
    Qty = models.CharField(max_length = 100)
    Keterangan = models.CharField(max_length = 100)
    Tggl_Pengiriman = models.CharField(max_length = 30)
    Mesin = models.CharField(max_length = 5)
  
