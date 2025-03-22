from django.db import models
from users.models import User
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order_type = models.CharField(max_length=4, choices=[('BUY', 'Buy'), ('SELL', 'Sell')])
    status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('EXECUTED', 'Executed')], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

class Transaction(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    executed_at = models.DateTimeField(auto_now_add=True)

class Balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    available_funds = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    holdings = models.JSONField(default=dict) 