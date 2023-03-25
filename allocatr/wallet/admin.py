from django.contrib import admin

from .models import Account, Budget, Category, Month, Transaction, UserSettings


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "currency",
        "start_day_of_month"
    )


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "first_day", "last_day")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "account_type",
        "current_balance",
        "active",
    )
    list_display_links = ("name",)
    list_filter = ("account_type", "active")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "group")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "transaction_type", "amount", "date", "account")
    list_display_links = ("title",)
    list_filter = ("transaction_type", "account")
    search_fields = ("title",)
    date_hierarchy = "date"


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "month", "budgeted_amount")
    list_filter = ("user", "month", "categories")
