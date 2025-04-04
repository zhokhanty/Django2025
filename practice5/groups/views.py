from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GroupExpense
from .forms import GroupExpenseForm

@login_required
def group_expense_list(request):
    """Выводит список групповых расходов"""
    expenses = GroupExpense.objects.all()
    return render(request, 'groups/group_expense_list.html', {'expenses': expenses})

@login_required
def add_group_expense(request):
    """Добавление группового расхода"""
    if request.method == 'POST':
        form = GroupExpenseForm(request.POST)
        if form.is_valid():
            group_expense = form.save()
            group_expense.users.add(request.user)  # Добавляем текущего пользователя
            return redirect('group_expense_list')
    else:
        form = GroupExpenseForm()
    return render(request, 'groups/add_group_expense.html', {'form': form})
