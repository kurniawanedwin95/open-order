from django import forms

from models import Order, Production, CmpltOrder

from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

class OrderEntryForm(forms.ModelForm):
    Nomor_PO = forms.CharField(required=True)
    Item_desc = forms.CharField() #akan dganti sama Product dan Keterangan Item
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required=False, initial=unicode(datetime.now().replace(microsecond=0)))
    
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
# ModelChoiceField returns an instance of an object
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
    Tggl_Pengiriman = forms.CharField(required=False, initial=unicode(datetime.now().replace(microsecond=0)))
    Mesin = forms.CharField()
    Tggl_Mulai_Produksi = forms.CharField(required=False, initial=unicode(datetime.now().replace(microsecond=0)))
    
    class Meta:
        model = Production
        fields = ('Nomor_PO', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Mesin', 'Tggl_Mulai_Produksi')
        widgets = {
            'Tggl_Pengiriman': DateInput(),
        }

class ProductionFinishForm(forms.Form):
    choices = [
        ('CoEx_2', 'CoEx 2'),
        ('CoEx_3', 'CoEx 3'),
        ('CoEx_4', 'CoEx 4'),
        ('CoEx_5', 'CoEx 5'),
        ('CoEx_6', 'CoEx 6'),
    ]
    
    production = Production.objects.all()
    Machine_ID = forms.ChoiceField(choices=choices)
    Nomor_PO = MyModelChoiceField(queryset=production, to_field_name="Nomor_PO")
    Batch_Output_Dalam_Ton = forms.CharField(required=True)
    Batch_Output_Dalam_Meter = forms.CharField(required=True)
    Batch_Output_Dalam_Roll = forms.CharField(required=True)
        
class OrderCompleteForm(forms.ModelForm):
    Nomor_PO = forms.CharField()
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required=False, initial=unicode(datetime.now().replace(microsecond=0)))
    Mesin = forms.CharField()
    Tggl_Mulai_Produksi = forms.CharField(required=False, initial=unicode(datetime.now().replace(microsecond=0)))
    Tggl_Selesai_Produksi = forms.CharField(required=False, initial=unicode(datetime.now().replace(microsecond=0)))
    Batch_Output_Berat = forms.CharField()
    Batch_Output_Panjang = forms.CharField()
    Batch_Output_Roll = forms.CharField()
    
    class Meta:
        model = CmpltOrder
        fields = ('Nomor_PO', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Mesin', 'Tggl_Mulai_Produksi', 'Tggl_Selesai_Produksi', 'Batch_Output_Berat', 'Batch_Output_Panjang', 'Batch_Output_Roll')

class HistoryQueryForm(forms.Form):
    choices = [
        ('Nomor_PO', 'Nomor PO'),
        ('Product', 'Product'),
        ('Keterangan_Item', 'Keterangan Item'),
        ('Item_desc', 'Item Desc'),
        ('U_of_m', 'U of m'),
        ('Qty', 'Quantity'),
        ('Keterangan', 'Keterangan'),
        ('Tggl_Pengiriman', 'Tanggal Pengiriman'),
        ('Mesin', 'Mesin'),
        ('Tggl_Mulai_Produksi', 'Tanggal Mulai Produksi'),
        ('Tggl_Selesai_Produksi', 'Tanggal Selesai Produksi'),
        ('Batch_Output_Berat', 'Batch Output Berat'),
        ('Batch_Output_Panjang', 'Batch Output Panjang'),
        ('Batch_Output_Roll', 'Batch Output Roll'),
    ]
    
    Query_Berdasarkan = forms.ChoiceField(choices=choices)
    Query_Keyword = forms.CharField()
    