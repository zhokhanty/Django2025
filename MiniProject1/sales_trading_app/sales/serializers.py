from rest_framework import serializers
from .models import SalesOrder, Invoice

class SalesOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrder
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'status', 'created_at']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'sales_order', 'invoice_number', 'issued_at']