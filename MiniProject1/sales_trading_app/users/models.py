from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('ADMIN', 'Admin'),
        ('TRADER', 'Trader'),
        ('SALES_REP', 'Sales Representative'),
        ('CUSTOMER', 'Customer'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='CUSTOMER')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)