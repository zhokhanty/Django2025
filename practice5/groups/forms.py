from django import forms
from .models import GroupExpense

class GroupExpenseForm(forms.ModelForm):
    class Meta:
        model = GroupExpense
        fields = ['name', 'amount', 'date', 'users']
