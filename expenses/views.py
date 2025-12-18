from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Expense
from .forms import ExpenseForm

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(e.amount for e in expenses)

    return render(request, 'expenses/dashboard.html', {
        "expenses": expenses,
        "total":total
    })

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect('expense_list')

    return render(request, 'expenses/confirm_delete.html', {'expense': expense})

