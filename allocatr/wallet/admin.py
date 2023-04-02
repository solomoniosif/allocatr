from django.contrib import admin

from .models import (
    Account,
    Budget,
    Category,
    Month,
    PlannedTransaction,
    Transaction,
    UserSettings,
)


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "currency", "start_day_of_month")


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
    list_display = ("__str__", "parent", "group", "get_hierarchy")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by("parent__id", "id")

    def get_hierarchy(self, obj):
        hierarchy = obj.name
        level = 0
        while obj.parent:
            level += 1
            obj = obj.parent
            hierarchy = obj.name + " » " + hierarchy
        return hierarchy

    get_hierarchy.short_description = "Hierarchy"
    get_hierarchy.admin_order_field = "parent__name"


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "transaction_type", "amount", "date", "account")
    list_display_links = ("title",)
    list_filter = ("transaction_type", "account")
    search_fields = ("title",)
    date_hierarchy = "date"


@admin.register(PlannedTransaction)
class PlannedTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "transaction_type",
        "amount",
        "date",
        "account",
        "is_duplicated",
    )


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "month", "budgeted_amount")
    list_filter = ("user", "month", "category")
