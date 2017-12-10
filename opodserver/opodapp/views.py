# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db import connection

from forms import OrderEntryForm, OrderModifyForm
from models import Order

# Create your views here.

def index(request):
    return render(request, "index.html")

# Class untuk menampilkan order yang ada, order yang di proses, dan output produksi di /
class OpenOrderView(TemplateView):
    template_name = "./index.html"
    
    def get(self, request):
        order = list(Order.objects.all())
        # print order[0].Nomor_PO
        print order
        return render(request, self.template_name, {'order': order})

# method False untuk Get request, True untuk Post
# Class untuk memasukan order di order_entry.html
class OrderEntryView(TemplateView):
    template_name = "./order_entry.html"
    
    def get(self, request):
        form = OrderEntryForm()
        return render(request, self.template_name, {'form': form, 'method': False})

    def post(self, request):
        form = OrderEntryForm(request.POST)
        if form.is_valid():
            form.save()
            Nomor_PO = form.cleaned_data['Nomor_PO']
            form = OrderEntryForm()
            return render(request, self.template_name, {'form': form, 'Nomor_PO': Nomor_PO, 'method': True})

        return render(request, self.template_name, {'form': form, 'method': False})

# Class untuk mengubah atau menghapus order di order_modify.html
class OrderModifyView(TemplateView):
    template_name = "./order_modify.html"
    
    def get(self, request):
        form = OrderModifyForm()
        return render(request, self.template_name, {'form': form, 'method': False})