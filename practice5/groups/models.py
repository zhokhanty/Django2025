from django.db import models
from django.contrib.auth.models import User

class GroupExpense(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    users = models.ManyToManyField(User)

    def split_expense(self):
        return self.amount / self.users.count()

    def __str__(self):
        return f"{self.name} - {self.amount}"
