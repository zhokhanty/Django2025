from django.urls import path
from .views import SalesOrderDetailView, InvoiceListView, generate_invoice_pdf, InvoiceCreateView

urlpatterns = [
    path('sales-orders/', InvoiceCreateView.as_view(), name='sales-order-list'),
    path('sales-orders/<int:pk>/', SalesOrderDetailView.as_view(), name='sales-order-detail'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
    path('invoices/<int:invoice_id>/pdf/', generate_invoice_pdf, name='invoice-pdf'),
]