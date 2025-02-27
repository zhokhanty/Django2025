from rest_framework import serializers
from .models import Order, Transaction

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'quantity', 'price', 'order_type', 'status', 'created_at']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'order', 'executed_at']