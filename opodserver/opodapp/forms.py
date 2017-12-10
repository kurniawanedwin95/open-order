from django import forms

from models import Order

class OrderEntryForm(forms.ModelForm):
    Nama_Order = forms.CharField()
    Nomor_PO = forms.CharField()
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required=False)
    
    class Meta:
        model = Order
        fields = ('Nama_Order', 'Nomor_PO', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman')

# subclass biar bisa display pake Nomor PO
class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.Nomor_PO
 
# nyari pake Nomor PO, nanti di pass ke OrderEntryForm
# ModelChoiceField milih an instance of an object
class OrderModifyForm(forms.ModelForm):
    order = Order.objects.all()
    Nomor_PO = MyModelChoiceField(queryset=order, to_field_name="Nomor_PO")
    
    class Meta:
        model = Order
        fields = ('Nomor_PO',)