# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from forms import OrderEntryForm

# Create your views here.

def index(request):
    return render(request, "index.html")
    
def order_entry(request):
    return render(request, "order_entry.html")
    
class OrderEntryView(TemplateView):
    template_name = "./order_entry.html"
    
    def get(self, request):
        form = OrderEntryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = OrderEntryForm(request.POST)
        if form.is_valid():
            form.save()
            Nomor_PO = form.cleaned_data['Nomor_PO']
            form = OrderEntryForm()
            return render(request, self.template_name, {'form': form, 'Nomor_PO': Nomor_PO})

        return render(request, self.template_name, {'form': form})
