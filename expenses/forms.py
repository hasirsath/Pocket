from django.forms import ModelForm
from .models import Expense, Budget
from django import forms

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'category', 'amount']
       


class BudgetForm(forms.ModelForm):
    month = forms.DateField(
        label="Month and Year",
        input_formats=['%Y-%m'],
        widget=forms.DateInput(
            attrs={'type': 'month'},
            format='%Y-%m'
        )
    )

    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month']

    def clean_month(self):
        date = self.cleaned_data['month']
        return date.replace(day=1)  # store first day of month
