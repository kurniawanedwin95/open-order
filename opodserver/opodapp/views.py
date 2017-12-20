# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django import forms

from forms import OrderEntryForm, OrderSelectForm, MachineSelectForm, OrderProductionForm, ProductionFinishForm, OrderCompleteForm
from models import Order, Production, CmpltOrder

from datetime import datetime

# Create your views here.

def index(request):
    return render(request, "index.html")

#---------------------------------OPEN-ORDER INDEX------------------------------------
# Class untuk menampilkan order yang ada, order yang di proses, dan output produksi di /
class OpenOrderView(TemplateView):
    template_name = "./index.html"
    
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

class SalesPortalView(TemplateView):
    template_name = "./sales_portal.html"
    def get(self, request):
        order = list(Order.objects.all())
        return render(request, self.template_name, {'order': order, })

class PPICPortalView(TemplateView):
    template_name = "./ppic_portal.html"
    def get(self, request):
        production = list(Production.objects.all())
        return render(request, self.template_name, {'production': production, })

#--------------------------------ORDER ENTRY&MODIFICATION-------------------------------
# method False untuk Get request, gagal masuk ke db; True untuk Post
# Class untuk memasukan order di order_entry.html
class OrderEntryView(TemplateView):
    template_name = "./order_entry.html"
    
    # untuk initial page load
    def get(self, request):
        form = OrderEntryForm()
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
            form = OrderEntryForm(initial={'Nomor_PO': order.Nomor_PO, 'Item_desc': order.Item_desc, 'U_of_m': order.U_of_m, 'Qty': order.Qty, 'Keterangan': order.Keterangan, 'Tggl_Pengiriman': order.Tggl_Pengiriman})
            form.fields['Nomor_PO'].widget = forms.HiddenInput()
        except ObjectDoesNotExist:
            print("Order tidak ditemukan")
            form = OrderEntryForm()
        return render(request, self.template_name, {'form': form, 'Nomor_PO': Nomor_PO, 'method': False})

    # untuk commit order modification
    def post(self, request):
        form = OrderEntryForm(request.POST)
        print form
        if form.is_valid():
            Nomor_PO = form.cleaned_data['Nomor_PO']
            former = Order.objects.get(Nomor_PO=Nomor_PO)
            former.Nomor_PO = Nomor_PO
            former.Item_desc = form.cleaned_data['Item_desc']
            former.U_of_m = form.cleaned_data['U_of_m']
            former.Qty = form.cleaned_data['Qty']
            former.Keterangan = form.cleaned_data['Keterangan']
            former.Tggl_Pengiriman = form.cleaned_data['Tggl_Pengiriman']
            former.save()
            print('Entry %s updated' % Nomor_PO)
        else:
            print('Update failed')
        return redirect('/')

#-----------------------------PRODUCTION ENTRY&MODIFICATION------------------------------
class MachineSelectView(TemplateView):
    template_name = "./machine_select.html"
    
    def get(self, request):
        if request.GET.get("Machine_ID"):
            Machine_ID = request.GET.get("Machine_ID")
            return redirect('/production_entry/?Machine_ID=%s' % Machine_ID)
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
        for Nomor_PO in Nomor_PO_list:
            # ngebuang character terakhir("/") di string Nomor_PO
            # Nomor_PO = Nomor_PO[:-1]
            order = Order.objects.get(Nomor_PO=Nomor_PO)
            data = {
                'Nomor_PO': Nomor_PO,
                'Item_desc': order.Item_desc,
                'U_of_m': order.U_of_m,
                'Qty': order.Qty,
                'Keterangan': order.Keterangan,
                'Tggl_Pengiriman': order.Tggl_Pengiriman,
                'Mesin': Machine_ID,
                'Tggl_Mulai_Produksi': unicode(datetime.now()),
            }
            form = OrderProductionForm(data)
            if form.is_valid():
                form.save()
                order.delete()
                print "%(x)s being worked on %(y)s" % {'x': Nomor_PO, 'y': Machine_ID}
            else:
                print "Form is not valid, something is wrong"
                return redirect('/')
        return redirect('/machine_select/')

class ProductionFinishView(TemplateView):
    template_name = "./production_finish.html"
    
    def get(self, request):
        form = ProductionFinishForm()
        return render(request, self.template_name, {'form': form, })
    
    def post(self, request):
        form = ProductionFinishForm(request.POST)
        if form.is_valid():
            Machine_ID = form.cleaned_data['Machine_ID']
            Nomor_PO = getattr(form.cleaned_data['Nomor_PO'],'Nomor_PO')
            print Nomor_PO
            if Production.objects.get(Mesin=Machine_ID, Nomor_PO=Nomor_PO):
                production = Production.objects.get(Mesin=Machine_ID, Nomor_PO=Nomor_PO)
                data = {
                    'Nomor_PO': production.Nomor_PO,
                    'Item_desc': production.Item_desc,
                    'U_of_m': production.U_of_m,
                    'Qty': production.Qty,
                    'Keterangan': production.Keterangan,
                    'Tggl_Pengiriman': production.Tggl_Pengiriman,
                    'Mesin': production.Mesin,
                    'Tggl_Mulai_Produksi': production.Tggl_Mulai_Produksi,
                    'Tggl_Selesai_Produksi': unicode(datetime.now()),
                    'Batch_Output_Berat': form.cleaned_data['Batch_Output_Dalam_Ton'],
                    'Batch_Output_Panjang': form.cleaned_data['Batch_Output_Dalam_Meter'],
                    'Batch_Output_Roll': form.cleaned_data['Batch_Output_Dalam_Roll'],
                }
                complete = OrderCompleteForm(data)
                complete.save()
                production.delete()
                print "%s finished production" % Machine_ID
            else:
                print "Machine not in production"
            form = ProductionFinishForm()
            return render(request, self.template_name, {'form': form})
        else:
            print "Form is invalid"
            return render(request, self.template_name)
