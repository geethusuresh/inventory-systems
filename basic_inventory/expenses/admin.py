from django.contrib import admin

from expenses.models import Expense, ExpenseHead

admin.site.register(Expense)
admin.site.register(ExpenseHead)