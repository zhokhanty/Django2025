from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from .forms import ExpenseForm, CategoryForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.utils.timezone import now


@login_required
def add_expense(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        date = request.POST.get("date")
        category_id = request.POST.get("category")

        category = Category.objects.get(id=category_id)

        Expense.objects.create(
            user=request.user,
            amount=amount,
            description=description,
            date=date,
            category=category
        )
        return redirect("expense_list")

    categories = Category.objects.filter(user=request.user)
    return render(request, "expenses/add_expense.html", {"categories": categories})


@login_required
def expense_list(request):
    """Выводит список расходов пользователя"""
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})


@login_required
def add_category(request):
    """Добавление новой категории"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('expense_list')
    else:
        form = CategoryForm()
    return render(request, 'expenses/add_category.html', {'form': form})
