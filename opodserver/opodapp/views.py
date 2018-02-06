# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django import forms

from forms import OrderEntryForm, OrderSelectForm, MachineSelectForm, OrderProductionForm, ProductionFinishForm, OrderCompleteForm, HistoryQueryForm, AddCustomerForm
from models import Order, Production, CmpltOrder, ProductList, CustomerList, SortedCustomerList

from datetime import datetime
import pytz

# Create your views here.

def index(request):
    return render(request, "index.html")

#---------------------------------OPEN-ORDER INDEX------------------------------------
# Class untuk menampilkan order yang ada, order yang di proses, dan output produksi di /
class OpenOrderView(TemplateView):
    template_name = "./index.html"
    
    def get(self, request):
        order = list(Order.objects.all())
        production = list(Production.objects.all().order_by('Tggl_Pengiriman'))
        # sudah ada produksi yang selesai
        if CmpltOrder.objects.first():
            complete = CmpltOrder.objects.latest('Tggl_Selesai_Produksi')
        # initial state, belom ada produksi yang selesai sama sekali
        else:
            data = {
                'Nomor_PO': "None",
                'Mesin': "None yet",
                'Tggl_Selesai_Produksi': 0,
                'Batch_Output_Berat': 0,
                'Batch_Output_Panjang': 0,
                'Batch_Output_Roll': 0,
                }
            complete = CmpltOrder(data)
        return render(request, self.template_name, {'order': order, 'production': production, 'complete': complete})

class SalesPortalView(TemplateView):
    template_name = "./sales_portal.html"
    def get(self, request):
        order = list(Order.objects.all())
        return render(request, self.template_name, {'order': order, })

class PPICPortalView(TemplateView):
    template_name = "./ppic_portal.html"
    def get(self, request):
        production = list(Production.objects.all().order_by('Tggl_Pengiriman'))
        return render(request, self.template_name, {'production': production, })

#--------------------------------ORDER ENTRY&MODIFICATION-------------------------------
# method False untuk Get request, gagal masuk ke db; True untuk Post
# Class untuk memasukan order di order_entry.html
class OrderEntryView(TemplateView):
    template_name = "./order_entry.html"
    
    # untuk initial page load
    def get(self, request):
        form = OrderEntryForm()
        # print form #debug
        return render(request, self.template_name, {'form': form, 'method': False})

    def post(self, request):
        form = OrderEntryForm(request.POST)
        if form.is_valid():
            Nomor_PO = form.cleaned_data['Nomor_PO']
            # check Nomor_PO sudah terpakai belom
            if Order.objects.filter(Nomor_PO=Nomor_PO).exists():
                form = OrderEntryForm()
                return render(request, self.template_name, {'form': form, 'method': False})
            # Order berhasil masuk
            else:
                # print form #debug
                form.save()
                form = OrderEntryForm()
                return render(request, self.template_name, {'form': form, 'Nomor_PO': Nomor_PO, 'method': True})

        return render(request, self.template_name, {'form': form, 'method': False})

# Class untuk mengubah atau menghapus order di order_modify.html
class OrderModifyView(TemplateView):
    template_name = "./order_modify.html"
    
    def get(self, request):
        # pass variable ke /modify
        if request.GET.get("Nomor_PO"):
            Nomor_PO = request.GET.get("Nomor_PO")
            return redirect('/modify/?Nomor_PO=%s' % Nomor_PO)
        # untuk initial page load
        else:
            form = OrderSelectForm()
            return render(request, self.template_name, {'form': form, 'method': False})
        
    def post(self, request):
        form = OrderSelectForm(request.POST)
        # untuk menghapus entry
        if form.is_valid():
            Nomor_PO = request.POST.get("Nomor_PO")
            order = Order.objects.get(Nomor_PO=Nomor_PO)
            order.delete()
            form = OrderSelectForm()
            return render(request, self.template_name, {'form': form, 'Nomor_PO': Nomor_PO, 'method': True})
        # default condition
        else:
            return render(request, self.template_name, {'form': form, 'method': True})
        
# Class untuk melakukan perubahan ke order
class ModificationView(TemplateView):
    template_name = "./modify.html"
    
    # terima variable dari order_modify
    def get(self, request):
        Nomor_PO = request.GET.get("Nomor_PO")
        try:
            order = Order.objects.get(Nomor_PO=Nomor_PO)
            form = OrderEntryForm(initial={'Nomor_PO': order.Nomor_PO, 'Customer_Name': order.Customer_Name, 'Product_Name': order.Product_Name, 'Item_desc': order.Item_desc, 'U_of_m': order.U_of_m, 'Qty': order.Qty, 'Keterangan': order.Keterangan, 'Tggl_Pengiriman': order.Tggl_Pengiriman})
            form.fields['Nomor_PO'].widget = forms.HiddenInput()
        except ObjectDoesNotExist:
            print("Order tidak ditemukan")
            form = OrderEntryForm()
        return render(request, self.template_name, {'form': form, 'Nomor_PO': Nomor_PO, 'method': False})

    # untuk commit order modification
    def post(self, request):
        form = OrderEntryForm(request.POST)
        # print form #debug
        if form.is_valid():
            Nomor_PO = form.cleaned_data['Nomor_PO']
            former = Order.objects.get(Nomor_PO=Nomor_PO)
            former.Nomor_PO = Nomor_PO
            former.Customer_Name = form.cleaned_data['Customer_Name']
            former.Product_Name = form.cleaned_data['Product_Name']
            former.Item_desc = form.cleaned_data['Item_desc']
            former.U_of_m = form.cleaned_data['U_of_m']
            former.Qty = form.cleaned_data['Qty']
            former.Keterangan = form.cleaned_data['Keterangan']
            former.Tggl_Pengiriman = form.cleaned_data['Tggl_Pengiriman']
            former.Tggl_Order_Masuk = form.cleaned_data['Tggl_Order_Masuk'] #remove to not update during modification
            former.save()
            print('Entry %s updated' % Nomor_PO)
        else:
            print('Update failed')
        return redirect('/sales_portal')

#-----------------------------PRODUCTION ENTRY&MODIFICATION------------------------------
class MachineSelectView(TemplateView):
    template_name = "./machine_select.html"
    
    def get(self, request):
        # machine selected
        if request.GET.get("Machine_ID"):
            Machine_ID = request.GET.get("Machine_ID")
            return redirect('/production_entry/?Machine_ID=%s' % Machine_ID)
        # initial load-in
        else:
            form = MachineSelectForm()
            return render(request, self.template_name, {'form': form, })
            
class ProductionEntryView(TemplateView):
    template_name = "./production_entry.html"
    
    def get(self, request):
        order = Order.objects.all()
        Machine_ID = request.GET.get("Machine_ID")
        print Machine_ID
        return render(request, self.template_name, {'order': order, 'Machine_ID': Machine_ID, 'method': False,})
    
    def post(self, request):
        Nomor_PO_list = request.POST.getlist("Nomor_PO")
        Machine_ID = request.POST.get("Machine_ID")
        production = Production.objects.all()
        for Nomor_PO in Nomor_PO_list:
            # ngebuang character terakhir("/") di string Nomor_PO
            # Nomor_PO = Nomor_PO[:-1]
            if Production.objects.filter(Nomor_PO=Nomor_PO,Mesin=Machine_ID).exists():
                print "%s not added, already in production/does not exist" % Nomor_PO
            else:
                order = Order.objects.get(Nomor_PO=Nomor_PO)
                data = {
                    'Nomor_PO': Nomor_PO,
                    'Customer_Name': order.Customer_Name,
                    'Product_Name': order.Product_Name,
                    'Item_desc': order.Item_desc,
                    'U_of_m': order.U_of_m,
                    'Qty': order.Qty,
                    'Keterangan': order.Keterangan,
                    'Tggl_Pengiriman': order.Tggl_Pengiriman,
                    'Tggl_Order_Masuk': order.Tggl_Order_Masuk,
                    'Mesin': Machine_ID,
                    'Tggl_Mulai_Produksi': unicode(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%m/%d/%Y %H:%M')),
                }
                form = OrderProductionForm(data)
                if form.is_valid():
                    form.save()
                    # order.delete() #mgkin jangan di delete dlu
                    print "%(x)s being worked on %(y)s" % {'x': Nomor_PO, 'y': Machine_ID}
                else:
                    print "Form is not valid, something is wrong"
                    return redirect('/')
        return redirect('/machine_select/')

class MachineSelectFinishView(TemplateView):
    template_name = "./machine_select_finish.html"
    
    def get(self, request):
        # machine selected
        if request.GET.get("Machine_ID"):
            Machine_ID = request.GET.get("Machine_ID")
            return redirect('/production_finish/?Machine_ID=%s' % Machine_ID)
        # initial load-in
        else:
            form = MachineSelectForm()
            return render(request, self.template_name, {'form': form, })

class ProductionFinishView(TemplateView):
    template_name = "./production_finish.html"
    
    def get(self, request):
        production = Production.objects.all()
        form = ProductionFinishForm()
        field_order = ['Machine_ID', 'Nomor_PO', 'Batch_Output_Dalam_Kg', 'Batch_Output_Dalam_Meter', 'Batch_Output_Dalam_Roll', 'Remarks']
        form.order_fields(field_order)
        return render(request, self.template_name, {'form': form, 'production': production, 'method':False})
    
    def post(self, request):
        form = ProductionFinishForm(request.POST)
        print form
        if form.is_valid():
            Machine_ID = form.cleaned_data['Machine_ID']
            # Nomor_PO as string
            Nomor_PO = form.cleaned_data['Nomor_PO']
            print Nomor_PO
            if Production.objects.get(Mesin=Machine_ID, Nomor_PO=Nomor_PO):
                production = Production.objects.get(Mesin=Machine_ID, Nomor_PO=Nomor_PO)
                data = {
                    'Nomor_PO': production.Nomor_PO,
                    'Customer_Name': production.Customer_Name,
                    'Product_Name': production.Product_Name,
                    'Item_desc': production.Item_desc,
                    'U_of_m': production.U_of_m,
                    'Qty': production.Qty,
                    'Keterangan': production.Keterangan,
                    'Tggl_Pengiriman': production.Tggl_Pengiriman,
                    'Tggl_Order_Masuk': production.Tggl_Order_Masuk,
                    'Mesin': production.Mesin,
                    'Tggl_Mulai_Produksi': production.Tggl_Mulai_Produksi,
                    'Tggl_Selesai_Produksi': unicode(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%m/%d/%Y %H:%M')),
                    'Batch_Output_Berat': form.cleaned_data['Batch_Output_Dalam_Kg'],
                    'Batch_Output_Panjang': form.cleaned_data['Batch_Output_Dalam_Meter'],
                    'Batch_Output_Roll': form.cleaned_data['Batch_Output_Dalam_Roll'],
                    'Remarks': form.cleaned_data['Remarks'],
                }
                complete = OrderCompleteForm(data)
                complete.save()
                production.delete()
                
                if Production.objects.filter(Nomor_PO=Nomor_PO).exists():
                    # gak ada yg diremove
                    print "%s is still in production in another machine" % Nomor_PO
                else:
                    order = Order.objects.get(Nomor_PO=Nomor_PO)
                    order.delete()
                    print "%s finished production" % Nomor_PO
                
                print "%s finished production" % Machine_ID
            else:
                print "Machine not in production"
            production = Production.objects.all()
            form = ProductionFinishForm()
            return render(request, self.template_name, {'form': form, 'production': production})
        else:
            print "Form is invalid"
            production = Production.objects.all()
            form = ProductionFinishForm()
            return render(request, self.template_name)

#----------------------------------HISTORY&DATABASE QUERY--------------------------------

class HistoryView(TemplateView):
    template_name = "./history.html"
    def get(self, request):
        complete = list(CmpltOrder.objects.all())
        return render(request, self.template_name, {'complete': complete, })

class HistoryQueryView(TemplateView):
    template_name = "./history_query.html"
    def get(self, request):
        if request.GET.get("Query_Berdasarkan") and request.GET.get("Query_Keyword"):
            query = request.GET.get("Query_Berdasarkan")
            keyword = request.GET.get("Query_Keyword")
            return redirect("/query_results/?query=%(x)s&keyword=%(y)s" % {'x': query, 'y': keyword})
        else:
            form = HistoryQueryForm()
            return render(request, self.template_name, {'form': form, })


class QueryResultsView(TemplateView):
    template_name = "./query_results.html"
    def get(self, request):
        query = request.GET.get("query")
        keyword = request.GET.get("keyword")
        column = query+'__'+'icontains'
        complete = list(CmpltOrder.objects.filter(**{column:keyword}))
        return render(request, self.template_name, {'complete': complete, })


# -----------------------------ADD CUSTOMER TO DATABASE----------------------------------
#-------------------------------------UNTESTED-------------------------------------------
class AddCustomerView(TemplateView):
    template_name= "./add_customer.html"
    def get(self, request):
        form = AddCustomerForm()
        return render(request, self.template_name, {'form': form, })
    
    def post(self, request):
        form = AddCustomerForm(request.POST)
        if form.is_valid():
            newcustomername = form.cleaned_data['New_Customer_Name']
            newcustomernumber = form.cleaned_data['New_Customer_Number']
            if SortedCustomerList.objects.filter(Sorted_Customer_Number=newcustomernumber).exists():
                print 'Error. Previously entered Customer Number entered.'
            else:
                sortedcustomer = SortedCustomerList(Sorted_Customer_Name=newcustomername, Sorted_Customer_Number=newcustomernumber)
                sortedcustomer.save()
        form = AddCustomerForm()
        return render(request, self.template_name, {'form': form})

# -------------------------VIEW TO TEST VISUAL ELEMENTS--------------------------------
class TestView(TemplateView):
    template_name = "./test.html"
    def get(self, request):
        order = list(Order.objects.all())
        production = list(Production.objects.all())
        # sudah ada produksi yang selesai
        if CmpltOrder.objects.first():
            complete = CmpltOrder.objects.latest('Tggl_Selesai_Produksi')
        # initial state, belom ada produksi yang selesai sama sekali
        else:
            data = {
                'Nomor_PO': "None",
                'Mesin': "None yet",
                'Tggl_Selesai_Produksi': 0,
                'Batch_Output_Berat': 0,
                'Batch_Output_Panjang': 0,
                'Batch_Output_Roll': 0,
                }
            complete = CmpltOrder(data)
        
        return render(request, self.template_name, {'order': order, 'production': production, 'complete': complete})