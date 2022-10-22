from django import forms
from django.contrib import admin

from .models import (
    Account,
    Budget,
    Category,
    Currency,
    Expense,
    Income,
    Transaction,
    Transfer,
)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name", "symbol", "code")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "type",
        "balance",
        "currency",
        "active",
        "exclude_from_budget",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "active")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("type", "title", "amount", "date", "account", "notes")
    list_filter = ("type", "account")
    search_fields = ("title",)
    date_hierarchy = "date"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "date", "account", "notes")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        income_categories = Category.objects.filter(group=Category.Group.INCOME)
        form.base_fields["category"].queryset = income_categories
        form.base_fields["type"].initial = "IN"
        form.base_fields["type"].widget = forms.HiddenInput()
        form.base_fields["dest_account"].widget = forms.HiddenInput()
        return form


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "date", "account", "notes")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        income_categories = Category.objects.filter(group=Category.Group.EXPENSE)
        form.base_fields["category"].queryset = income_categories
        form.base_fields["type"].initial = "EX"
        form.base_fields["type"].widget = forms.HiddenInput()
        form.base_fields["dest_account"].widget = forms.HiddenInput()
        return form


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("title", "amount", "date", "account", "dest_account", "notes")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        income_categories = Category.objects.filter(group=Category.Group.TRANSFER)
        form.base_fields["category"].queryset = income_categories
        form.base_fields["type"].initial = "TR"
        form.base_fields["type"].widget = forms.HiddenInput()
        form.base_fields["account"].label = "Source account"
        form.base_fields["dest_account"].label = "Destination account"
        return form


admin.site.register(Budget)
