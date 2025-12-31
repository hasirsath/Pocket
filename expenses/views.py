from calendar import month
from unicodedata import category
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from .models import Expense, Budget
from .forms import ExpenseForm, BudgetForm
from django.db.models import Sum
from datetime import date

current_month = date.today().replace(day=1)

@login_required
def dashboard(request):
    today = date.today()

    # All expenses of logged-in user
    expenses = Expense.objects.filter(user=request.user)

    # Total spent (all time)
    total_spent = expenses.aggregate(total=Sum('amount'))['total'] or 0

    # Current month expenses
    monthly_expenses = expenses.filter(
        date__year=today.year,
        date__month=today.month
    )

    monthly_total = monthly_expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # Budgets for current month
    budgets = Budget.objects.filter(
        user=request.user,
        month__year=today.year,
        month__month=today.month
    )

    budget_data = []

    for budget in budgets:
        spent = monthly_expenses.filter(
            category=budget.category
        ).aggregate(total=Sum('amount'))['total'] or 0

        budget_data.append({
            'category': budget.category.name,
            'budget': budget.amount,
            'spent': spent,
            'remaining': budget.amount - spent,
            'exceeded': spent > budget.amount
        })

    # Recent 5 expenses only
    recent_expenses = expenses.order_by('-date')[:5]

    category_expenses = (
    monthly_expenses
    .values('category__name')
    .annotate(total=Sum('amount'))
)

    pie_labels = [c['category__name'] for c in category_expenses]
    pie_values = [float(c['total']) for c in category_expenses]


    return render(request, 'expenses/dashboard.html', {
        'total_spent': total_spent,
        'monthly_total': monthly_total,
        'budget_data': budget_data,
        'expenses': recent_expenses,
        'current_month': today.strftime('%B %Y'),
        'pie_labels': pie_labels,
        'pie_values': pie_values,
    })


@login_required
def expense_list(request):
    view_type = request.GET.get('view', 'all')

    expenses = Expense.objects.filter(user=request.user)

    monthly_expenses = None

    if view_type == 'monthly':
        monthly_expenses = (
            expenses
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('-month')
        )

    return render(request, 'expenses/expense_list.html', {
        'expenses': expenses,
        'monthly_expenses': monthly_expenses,
        'view_type': view_type
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
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect('dashboard')

    return render(request, 'expenses/confirm_delete.html', {'expense': expense})




@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user)
    data = []

    for b in budgets:
        spent = Expense.objects.filter(
            user=request.user,
            category=b.category,
            date__year=b.month.year,
            date__month=b.month.month
        ).aggregate(total=Sum('amount'))['total'] or 0

        data.append({
            'budget': b,
            'spent': spent,
            'remaining': b.amount - spent,
            'overspent': spent > b.amount
        })

    return render(request, 'expenses/budget_list.html', {'data': data})


@login_required
def add_budget(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)

        if form.is_valid():
            category = form.cleaned_data['category']
            amount = form.cleaned_data['amount']
            month = form.cleaned_data['month'].replace(day=1)

            Budget.objects.update_or_create(
                user=request.user,
                category=category,
                month=month,
                defaults={
                    'amount': amount
                }
            )

            existing = Budget.objects.filter(
            user=request.user,
            category=category,
            month=month
            ).first()

            if existing:
                existing.amount = amount
                existing.save()
        else:
            Budget.objects.create(
        user=request.user,
        category=category,
        month=month,
        amount=amount
    )


        return redirect('budget_list')

    else:
        form = BudgetForm()

    return render(request, 'expenses/budget_form.html', {
        'form': form
    })


@login_required
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)

    if request.method == 'POST':
        budget.delete()

    return redirect('budget_list')


@login_required
def edit_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('budget_list')
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'expenses/budget_form.html', {'form': form})

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

