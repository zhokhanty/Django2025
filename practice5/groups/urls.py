from django.urls import path
from .views import group_expense_list, add_group_expense

urlpatterns = [
    path('', group_expense_list, name='group_expense_list'),
    path('add/', add_group_expense, name='add_group_expense'),
]
