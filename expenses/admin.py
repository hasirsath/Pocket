from django.contrib import admin
from .models import Budget
from .models import Category    

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'month')

admin.site.register(Category)
