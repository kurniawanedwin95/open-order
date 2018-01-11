from django import forms

from models import Order, Production, CmpltOrder, ProductList, CustomerList

from datetime import datetime

class DateInput(forms.DateInput):
    input_type = 'date'

# subclass biar bisa display pake Nomor PO
class NomorPOChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.Nomor_PO

class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.Product_Name

class OrderEntryForm(forms.ModelForm):
    Nomor_PO = forms.CharField(required=True)
    products = ProductList.objects.all()
    Product_Name = ProductChoiceField(queryset=products, to_field_name="Product_Name")
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required=False, initial=unicode(datetime.now().replace(microsecond=0)))
    
    class Meta:
        model = Order
        fields = ('Nomor_PO', 'Product_Name', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman')
        widgets = {
            'Tggl_Pengiriman': DateInput(),
        }
        # widgets = {
        #     'Tggl_Pengiriman': forms.TextInput(attrs={'placeholder': 'dd/mm/yy'}),
        # }
    
    # Ngubah ProductList Object jadi Product_Name doang pas di form.save()
    def clean_Product_Name(self):
        data = self.cleaned_data['Product_Name'].Product_Name
        return data

# nyari pake Nomor PO, nanti di pass ke OrderEntryForm
# ModelChoiceField returns an instance of an object
class OrderSelectForm(forms.ModelForm):
    order = Order.objects.all()
    Nomor_PO = NomorPOChoiceField(queryset=order, to_field_name="Nomor_PO")
    
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
    Product_Name = forms.CharField()
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required=False, initial=unicode(datetime.now().replace(microsecond=0)))
    Mesin = forms.CharField()
    Tggl_Mulai_Produksi = forms.CharField(required=False, initial=unicode(datetime.now().replace(microsecond=0)))
    
    class Meta:
        model = Production
        fields = ('Nomor_PO', 'Product_Name', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Mesin', 'Tggl_Mulai_Produksi')
        widgets = {
            'Tggl_Pengiriman': DateInput(),
        }

class ProductionFinishForm(forms.Form):
    # def __init__(self,*args,**kwargs):
    #     Machine_ID = kwargs.pop('Machine_ID')
    #     super(ProductionFinishForm,self).__init__(*args,**kwargs)
    #     self.fields['Machine_ID'].widget = forms.TextInput(attrs={'Machine_ID':Machine_ID})
    #     production = Production.objects.filter(Machine_ID=self.Machine)
    #     self.fields['Nomor_PO'].widget = NomorPOChoiceField(queryset = production, to_field_name="Nomor_PO")
    
    choices = [
        ('CoEx_2', 'CoEx 2'),
        ('CoEx_3', 'CoEx 3'),
        ('CoEx_4', 'CoEx 4'),
        ('CoEx_5', 'CoEx 5'),
        ('CoEx_6', 'CoEx 6'),
    ]
    
    production = Production.objects.all()
    # production = Production.objects.filter(Machine_ID=self.Machine)
    Machine_ID = forms.ChoiceField(choices=choices)
    # Machine_ID = forms.CharField()
    Nomor_PO = NomorPOChoiceField(queryset=production, to_field_name="Nomor_PO")
    Batch_Output_Dalam_Ton = forms.CharField(required=True)
    Batch_Output_Dalam_Meter = forms.CharField(required=True)
    Batch_Output_Dalam_Roll = forms.CharField(required=True)
        
class OrderCompleteForm(forms.ModelForm):
    Nomor_PO = forms.CharField()
    Product_Name = forms.CharField()
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
        fields = ('Nomor_PO', 'Product_Name', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Mesin', 'Tggl_Mulai_Produksi', 'Tggl_Selesai_Produksi', 'Batch_Output_Berat', 'Batch_Output_Panjang', 'Batch_Output_Roll')

class HistoryQueryForm(forms.Form):
    choices = [
        ('Nomor_PO', 'Nomor PO'),
        ('Product_Name', 'Product Name'),
        ('Product_Thickness', 'Product Thickness'),
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
    