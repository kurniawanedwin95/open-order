from django import forms

from models import Order, Production, CmpltOrder, ProductList, CustomerList, SortedCustomerList

from datetime import datetime
import pytz

class DateInput(forms.DateInput):
    input_type = 'date'

# subclass biar bisa display pake Nomor PO
class NomorPOChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.Nomor_PO

class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.Product_Name

class CustomerNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.Sorted_Customer_Name

class OrderEntryForm(forms.ModelForm):
    Nomor_PO = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. 4500705874 SMG'}))
    sorted_customer = SortedCustomerList.objects.all()
    Customer_Name = CustomerNameChoiceField(queryset=sorted_customer, to_field_name="Sorted_Customer_Name")
    
    # typeable for quick selection
    products = ProductList.objects.all()
    Product_Name = ProductChoiceField(queryset=products, to_field_name="Product_Name")
    
    # fallback method
    # Product_Name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. QUASAREX 01'}))
    
    Item_desc = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'cust. info/order spec', 'rows':3, 'cols': 30}))
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    
    class Meta:
        model = Order
        fields = ('Nomor_PO', 'Customer_Name', 'Product_Name', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman')

    # Ngubah ProductList Object jadi Product_Name doang pas di form.save() n upper case
    def clean_Customer_Name(self):
        data = self.cleaned_data['Customer_Name'].Sorted_Customer_Name
        # data = self.cleaned_data['Product_Name'].upper()
        return data

    # Ngubah ProductList Object jadi Product_Name doang pas di form.save() n upper case
    def clean_Product_Name(self):
        data = self.cleaned_data['Product_Name'].Product_Name
        return data
    
    # Ngubah U of M to uppercase pas di form.save() for consistency
    def clean_U_of_m(self):
        data = self.cleaned_data['U_of_m'].upper()
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
    Customer_Name = forms.CharField()
    Product_Name = forms.CharField()
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField()
    Mesin = forms.CharField()
    Tggl_Mulai_Produksi = forms.CharField(required=True, initial=unicode(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%m/%d/%Y %H:%M')))
    
    class Meta:
        model = Production
        fields = ('Nomor_PO', 'Customer_Name', 'Product_Name', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Mesin', 'Tggl_Mulai_Produksi')


class ProductionFinishForm(forms.Form):
    # failed trial to pass argument into form
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
    
    # production = Production.objects.values('Nomor_PO').distinct()
    production = Production.objects.all()
    Machine_ID = forms.ChoiceField(choices=choices)
    # to field name Nomor PO tpi isinya hrus beda
    Nomor_PO = NomorPOChoiceField(queryset=production, to_field_name="Nomor_PO")
    Batch_Output_Dalam_Ton = forms.CharField(required=True)
    Batch_Output_Dalam_Meter = forms.CharField(required=True)
    Batch_Output_Dalam_Roll = forms.CharField(required=True)
        
class OrderCompleteForm(forms.ModelForm):
    Nomor_PO = forms.CharField()
    Customer_Name = forms.CharField()
    Product_Name = forms.CharField()
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField()
    Mesin = forms.CharField()
    Tggl_Mulai_Produksi = forms.CharField()
    Tggl_Selesai_Produksi = forms.CharField(required=True, initial=unicode(datetime.now(pytz.timezone('Asia/Jakarta')).replace(microsecond=0)))
    Batch_Output_Berat = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 10'}))
    Batch_Output_Panjang = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 100'}))
    Batch_Output_Roll = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 5'}))
    
    class Meta:
        model = CmpltOrder
        fields = ('Nomor_PO', 'Customer_Name', 'Product_Name', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Mesin', 'Tggl_Mulai_Produksi', 'Tggl_Selesai_Produksi', 'Batch_Output_Berat', 'Batch_Output_Panjang', 'Batch_Output_Roll')

class HistoryQueryForm(forms.Form):
    choices = [
        ('Nomor_PO', 'Nomor PO'),
        ('Customer_Name', 'Customer Name'),
        ('Product_Name', 'Product Name'),
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
    