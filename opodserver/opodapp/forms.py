from django import forms

from models import Order

class OrderEntryForm(forms.Form):
  Nama_Order = forms.CharField()
  Nomor_PO = forms.CharField()
  Item_desc = forms.CharField()
  U_of_M = forms.CharField()
  Qty = forms.CharField()
  Keterangan = forms.CharField()
  Tggl_Pengiriman = forms.CharField(required = False)
  
  class Meta:
      model = Order
      fields = ('order',)
      
