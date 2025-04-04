from django.urls import path,include
from .views import expense_list, add_expense, add_category

urlpatterns = [
    path('', expense_list, name='expense_list'),
    path('add/', add_expense, name='add_expense'),
    path('category/add/', add_category, name='add_category'),
]

