from django import forms

from models import Order

class OrderEntryForm(forms.ModelForm):
    Nama_Order = forms.CharField()
    Nomor_PO = forms.CharField()
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required = False)
    
    class Meta:
        model = Order
        fields = ('Nama_Order', 'Nomor_PO', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman')
      
