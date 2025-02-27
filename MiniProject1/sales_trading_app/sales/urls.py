from django.urls import path
from .views import SalesOrderListCreateView, SalesOrderDetailView, InvoiceListView

urlpatterns = [
    path('sales-orders/', SalesOrderListCreateView.as_view(), name='sales-order-list'),
    path('sales-orders/<int:pk>/', SalesOrderDetailView.as_view(), name='sales-order-detail'),
    path('invoices/', InvoiceListView.as_view(), name='invoice-list'),
]