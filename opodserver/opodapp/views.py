# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
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
        form = OrderEntryForm()
        return render(request, self.template_name, {'form': form})
