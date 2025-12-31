from . import views
from django.urls import include, path
from .views import dashboard, add_expense

urlpatterns = [
    
    path('dashboard/', dashboard, name='dashboard'),
    path('', include('accounts.urls')),
    path('dashboard/', dashboard, name='dashboard'),
    path("add/", add_expense, name="add_expense"),
    path('expense/', views.expense_list, name='expense_list'),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
    path('budgets/', views.budget_list, name='budget_list'),
    path('budgets/add/', views.add_budget, name='add_budget'),
    path('budgets/edit/<int:pk>', views.edit_budget, name='edit_budget'),
    path('budgets/delete/<int:pk>', views.delete_budget, name='delete_budget'),

]