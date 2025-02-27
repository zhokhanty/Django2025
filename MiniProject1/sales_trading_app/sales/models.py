from django.db import models
from users.models import User
from products.models import Product

class SalesOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved')], default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100)
    issued_at = models.DateTimeField(auto_now_add=True)