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

# class NomorPOChoiceField2(forms.ModelChoiceField):
#     def label_from_instance(self, obj):
#         return "%s" % obj

class ProductChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.Product_Name

class CustomerNameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.Sorted_Customer_Name

class OrderEntryForm(forms.ModelForm):
    Nomor_PO = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. 4500705874 SMG'}))
    sorted_customer = SortedCustomerList.objects.all().order_by('Sorted_Customer_Number')
    Customer_Name = CustomerNameChoiceField(queryset=sorted_customer, to_field_name="Sorted_Customer_Name")
    
    # typeable for quick selection
    # products = ProductList.objects.all()
    # Product_Name = ProductChoiceField(queryset=products, to_field_name="Product_Name")
    
    # fallback method, capable of multiple entries
    Product_Name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'e.g. QUASAREX 01, BOLIDEX 03', 'size': 50}))
    
    Item_desc = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'cust. info/order spec', 'rows':3, 'cols': 30}))
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'datepicker'}))
    Tggl_Order_Masuk = forms.CharField(widget=forms.HiddenInput(), initial=unicode(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%m/%d/%Y %H:%M')))
    
    class Meta:
        model = Order
        fields = ('Nomor_PO', 'Customer_Name', 'Product_Name', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Tggl_Order_Masuk')

    def clean_Nomor_PO(self):
        data = self.cleaned_data['Nomor_PO']
        data = data.replace(";", "")
        data = data.replace("&", "")
        data = data.replace('"','')
        return data

    # Ngubah ProductList Object jadi Product_Name doang pas di form.save() n upper case
    def clean_Customer_Name(self):
        data = self.cleaned_data['Customer_Name'].Sorted_Customer_Name
        # data = self.cleaned_data['Product_Name'].upper()
        return data

    # Ngubah ProductList Object jadi Product_Name doang pas di form.save() n upper case
    def clean_Product_Name(self):
        data = self.cleaned_data['Product_Name'].upper()
        # data = self.cleaned_data['Product_Name'].Product_Name
        return data
    
    # Ngubah U of M to uppercase pas di form.save() for consistency
    def clean_U_of_m(self):
        data = self.cleaned_data['U_of_m'].upper()
        return data
    
    def clean_Tggl_Order_Masuk(self):
        data = unicode(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%m/%d/%Y %H:%M'))
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
    Tggl_Order_Masuk = forms.CharField()
    Mesin = forms.CharField()
    Tggl_Mulai_Produksi = forms.CharField(required=True, initial=unicode(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%m/%d/%Y %H:%M')))
    
    class Meta:
        model = Production
        fields = ('Nomor_PO', 'Customer_Name', 'Product_Name', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Tggl_Order_Masuk', 'Mesin', 'Tggl_Mulai_Produksi')


class ProductionFinishForm(forms.Form):
    choices = [
        ('CoEx_2', 'CoEx 2'),
        ('CoEx_3', 'CoEx 3'),
        ('CoEx_4', 'CoEx 4'),
        ('CoEx_5', 'CoEx 5'),
        ('CoEx_6', 'CoEx 6'),
    ]

    Machine_ID = forms.ChoiceField(choices=choices)
    
    
    production = [(str(p.Nomor_PO), str(p.Nomor_PO)) for p in Production.objects.raw('SELECT id, Nomor_PO from opodapp_production')]
    Nomor_PO = forms.ChoiceField(choices=production)
    
    # Nomor_PO = forms.CharField() #isi sendiri
    
    Batch_Output_Dalam_Kg = forms.CharField(required=True)
    Batch_Output_Dalam_Meter = forms.CharField(required=True)
    Batch_Output_Dalam_Roll = forms.CharField(required=True)

# ---------------------------------------UNUSED------------------------------------------
    # to field name Nomor PO tpi isinya hrus beda
    # production = Production.objects.values('Nomor_PO').distinct()
    # Nomor_PO = NomorPOChoiceField2(queryset=production, to_field_name="Nomor_PO")

    # def clean_Nomor_PO(self):
    #     # clean up the strings
        
    #     # <option value="{&#39;Nomor_PO&#39;: u&#39;2018TEST15&#39;}" selected>{&#39;Nomor_PO&#39;: u&#39;2018TEST15&#39;}</option>
        
    #     data = self.cleaned_data['Nomor_PO']
    #     # # splits by " mark and takes data between said character
    #     # data = data.split('"')[1]
    #     # # truncates the ending 6 characters
    #     # data = data[:-6]
    #     # # truncates the beginning 27 characters
    #     # data = data[27:]
        
    #     # other method
    #     data = data.split('"')[1]
    #     data = data.split(';')[3]
    #     data = data.split('&')[0]
        
    #     return data
# --------------------------------------------------------------------------------------
    
class OrderCompleteForm(forms.ModelForm):
    Nomor_PO = forms.CharField()
    Customer_Name = forms.CharField()
    Product_Name = forms.CharField()
    Item_desc = forms.CharField()
    U_of_m = forms.CharField()
    Qty = forms.CharField()
    Keterangan = forms.CharField()
    Tggl_Pengiriman = forms.CharField()
    Tggl_Order_Masuk = forms.CharField()
    Mesin = forms.CharField()
    Tggl_Mulai_Produksi = forms.CharField()
    Tggl_Selesai_Produksi = forms.CharField(required=True, initial=unicode(datetime.now(pytz.timezone('Asia/Jakarta')).replace(microsecond=0)))
    Batch_Output_Berat = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 10'}))
    Batch_Output_Panjang = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 100'}))
    Batch_Output_Roll = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g. 5'}))
    
    class Meta:
        model = CmpltOrder
        fields = ('Nomor_PO', 'Customer_Name', 'Product_Name', 'Item_desc', 'U_of_m', 'Qty', 'Keterangan', 'Tggl_Pengiriman', 'Tggl_Order_Masuk', 'Mesin', 'Tggl_Mulai_Produksi', 'Tggl_Selesai_Produksi', 'Batch_Output_Berat', 'Batch_Output_Panjang', 'Batch_Output_Roll')

class HistoryQueryForm(forms.Form):
    choices = [
        ('Nomor_PO', 'Nomor PO'),
        ('Sorted_Customer_Name', 'Customer Name'),
        ('Product_Name', 'Product Name'),
        ('Item_desc', 'Item Desc'),
        ('U_of_m', 'U of m'),
        ('Qty', 'Quantity'),
        ('Keterangan', 'Keterangan'),
        ('Tggl_Pengiriman', 'Tanggal Pengiriman'),
        ('Tggl_Order_Masuk', 'Tanggal Order Masuk'),
        ('Mesin', 'Mesin'),
        ('Tggl_Mulai_Produksi', 'Tanggal Mulai Produksi'),
        ('Tggl_Selesai_Produksi', 'Tanggal Selesai Produksi'),
        ('Batch_Output_Berat', 'Batch Output Berat'),
        ('Batch_Output_Panjang', 'Batch Output Panjang'),
        ('Batch_Output_Roll', 'Batch Output Roll'),
    ]
    
    Query_Berdasarkan = forms.ChoiceField(choices=choices)
    Query_Keyword = forms.CharField()

class AddCustomerForm(forms.Form):
    # Sorted_Customer_Name = forms.CharField(widget=forms.TextInput(attrs={'label': 'Customer Name'}))
    # Sorted_Customer_Number = forms.CharField(widget=forms.TextInput(attrs={'label': 'Customer Number'}))
    New_Customer_Name = forms.CharField()
    New_Customer_Number = forms.CharField()
    
    # class Meta:
    #     model = SortedCustomerList
    #     fields = ('Sorted_Customer_Name', 'Sorted_Customer_Number')
    #     labels = {
    #         'Sorted_Customer_Name': 'Customer Name',
    #         'Sorted_Customer_Number': 'Customer Number'
    #     }
        