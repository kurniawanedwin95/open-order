"""opodserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from opodapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.OpenOrderView.as_view(), name='index'),
    url(r'^order_entry/', views.OrderEntryView.as_view(), name='order_entry'),
    url(r'^order_modify/', views.OrderModifyView.as_view(), name='order_modify'),
    url(r'^modify/', views.ModificationView.as_view(), name='modify'),
    url(r'^machine_select/', views.MachineSelectView.as_view(), name='machine_select'),
    url(r'^production_entry/', views.ProductionEntryView.as_view(), name='production_entry'),
    url(r'^sales_portal/', views.SalesPortalView.as_view(), name='sales_portal'),
    url(r'^ppic_portal/', views.PPICPortalView.as_view(), name='ppic_portal'),
    url(r'^production_finish/', views.ProductionFinishView.as_view(), name='production_finish'),
    url(r'^history/', views.HistoryView.as_view(), name='history'),
    url(r'^history_query/', views.HistoryQueryView.as_view(), name='history_query'),
    url(r'^query_results/', views.QueryResultsView.as_view(), name='query_results'),
    url(r'^add_customer/', views.AddCustomerView.as_view(), name='add_customer'),
    url(r'^test/', views.TestView.as_view(), name='test'),
]
