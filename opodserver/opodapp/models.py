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
    Tggl_Pengiriman = models.CharField(max_length = 50)
    
class Production(models.Model):
    Nomor_PO = models.CharField(max_length = 100)
    Item_desc = models.CharField(max_length = 100)
    U_of_m = models.CharField(max_length = 10)
    Qty = models.CharField(max_length = 100)
    Keterangan = models.CharField(max_length = 100)
    Tggl_Pengiriman = models.CharField(max_length = 50)
    Mesin = models.CharField(max_length = 10)
    Tggl_Mulai_Produksi = models.CharField(max_length = 100)

class CmpltOrder(models.Model):
    Nomor_PO = models.CharField(max_length = 100)
    Item_desc = models.CharField(max_length = 100)
    U_of_m = models.CharField(max_length = 10)
    Qty = models.CharField(max_length = 100)
    Keterangan = models.CharField(max_length = 100)
    Tggl_Pengiriman = models.CharField(max_length = 100)
    Mesin = models.CharField(max_length = 10)
    Tggl_Mulai_Produksi = models.CharField(max_length = 100)
    Tggl_Selesai_Produksi = models.CharField(max_length = 100)
    Batch_Output_Berat = models.CharField(max_length = 100)
    Batch_Output_Panjang = models.CharField(max_length = 100)
    Batch_Output_Roll = models.CharField(max_length = 100)
