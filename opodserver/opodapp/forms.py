from django import forms

from models import Order, Production

from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderEntryForm(forms.ModelForm):
    Nomor_PO = forms.CharField()
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required=False, initial="24 December 2017")
    
    class Meta:
        model = Order
        fields = ('Nomor_PO', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman')
        widgets = {
            'Tggl_Pengiriman': DateInput(),
        }
        # widgets = {
        #     'Tggl_Pengiriman': forms.TextInput(attrs={'placeholder': 'dd/mm/yy'}),
        # }

# subclass biar bisa display pake Nomor PO
class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.Nomor_PO
 
# nyari pake Nomor PO, nanti di pass ke OrderEntryForm
# ModelChoiceField milih an instance of an object
class OrderSelectForm(forms.ModelForm):
    order = Order.objects.all()
    Nomor_PO = MyModelChoiceField(queryset=order, to_field_name="Nomor_PO")
    
    class Meta:
        model = Order
        fields = ('Nomor_PO',)
    

class MachineSelectForm(forms.Form):
    choices = [
        ('CoEx_2', 'CoEx 2'),
        ('CoEx_3', 'CoEx 3'),
        ('CoEx_4', 'CoEx 4'),
        ('CoEx_5', 'CoEx 5'),
        ('CoEx_6', 'CoEx 6'),
    ]
    Machine_ID = forms.ChoiceField(choices=choices)

class OrderProductionForm(forms.ModelForm):
    Nomor_PO = forms.CharField()
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required=False, initial="24 December 2017")
    Mesin = forms.CharField()
    Tggl_Mulai_Produksi = forms.CharField(required=False, initial="24-12-2017 00:00:00")
    
    class Meta:
        model = Production
        fields = ('Nomor_PO', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Mesin', 'Tggl_Mulai_Produksi')
        widgets = {
            'Tggl_Pengiriman': DateInput(),
        }

