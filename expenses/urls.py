from . import views
from django.urls import path
from .views import dashboard, add_expense

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path("add/", add_expense, name="add_expense"),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
]