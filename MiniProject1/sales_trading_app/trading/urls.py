from django.urls import path
from .views import OrderListCreateView, OrderDetailView, TransactionListView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
]