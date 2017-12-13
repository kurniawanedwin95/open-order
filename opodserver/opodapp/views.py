# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django import forms

from forms import OrderEntryForm, OrderSelectForm, OrderModifyForm
from models import Order

# Create your views here.

def index(request):
    return render(request, "index.html")

# Class untuk menampilkan order yang ada, order yang di proses, dan output produksi di /
class OpenOrderView(TemplateView):
    template_name = "./index.html"
    
    def get(self, request):
        order = list(Order.objects.all())
        return render(request, self.template_name, {'order': order})

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
    