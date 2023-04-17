from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Account, Budget, Category, PlannedTransaction, Transaction


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "title",
            "amount",
            "date",
            "account",
            "category",
            "notes",
            "transaction_type",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        income_categories = Category.objects.filter(group=Category.Group.INCOME)
        self.fields["category"].queryset = income_categories
        self.fields["transaction_type"].initial = "IN"
        self.fields["transaction_type"].widget = forms.HiddenInput()
        self.fields["date"].initial = timezone.now()


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "title",
            "amount",
            "date",
            "account",
            "category",
            "notes",
            "transaction_type",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        expense_categories = Category.objects.filter(group=Category.Group.EXPENSE)
        self.fields["category"].queryset = expense_categories
        self.fields["transaction_type"].initial = "EX"
        self.fields["transaction_type"].widget = forms.HiddenInput()
        self.fields["date"].initial = timezone.now()


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "title",
            "amount",
            "date",
            "account",
            "to_account",
            "category",
            "notes",
            "transaction_type",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        transfer_categories = Category.objects.filter(group=Category.Group.TRANSFER)
        transfer_category = Category.objects.get_or_create(
            name="Transfer", group=Category.Group.TRANSFER
        )[0]
        self.fields["title"].initial = "Transfer"
        self.fields["category"].queryset = transfer_categories
        self.fields["category"].initial = transfer_category
        self.fields["transaction_type"].initial = "TR"
        self.fields["transaction_type"].widget = forms.HiddenInput()
        self.fields["date"].initial = timezone.now()
        self.fields["account"].label = "Source account"
        self.fields["to_account"].label = "Destination account"

    def clean_title(self):
        value = self.cleaned_data.get("title")
        if not value or value == "Transfer":
            computed_title = self.compute_title()
            return computed_title
        return value

    def compute_title(self):
        account_pk = self.data.get("account")
        account = Account.objects.get(pk=account_pk)
        to_account_pk = self.data.get("to_account")
        to_account = Account.objects.get(pk=to_account_pk)
        return f"Transfer from {account} to {to_account}"


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            "name",
            "account_type",
            "current_balance",
            "balance_can_be_negative",
            "active",
            "exclude_from_budget",
            "show_on_dashboard",
            "color",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["color"].widget = forms.TextInput()


class AccountBalanceForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ("current_balance",)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("group", "name", "color", "active", "parent")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["color"].widget = forms.TextInput()


class PlannedIncomeForm(forms.ModelForm):
    class Meta:
        model = PlannedTransaction
        fields = {
            "title",
            "amount",
            "date",
            "account",
            "category",
            "notes",
            "transaction_type",
            "is_recurring",
            "recurrence_frequency",
            "is_completed",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        income_categories = Category.objects.filter(group=Category.Group.INCOME)
        self.fields["category"].queryset = income_categories
        self.fields["transaction_type"].initial = "IN"
        self.fields["transaction_type"].widget = forms.HiddenInput()
        self.fields["date"].initial = timezone.now()


class PlannedExpenseForm(forms.ModelForm):
    class Meta:
        model = PlannedTransaction
        fields = {
            "title",
            "amount",
            "date",
            "account",
            "category",
            "notes",
            "transaction_type",
            "is_recurring",
            "recurrence_frequency",
            "is_completed",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        expense_categories = Category.objects.filter(group=Category.Group.EXPENSE)
        self.fields["category"].queryset = expense_categories
        self.fields["transaction_type"].initial = "EX"
        self.fields["transaction_type"].widget = forms.HiddenInput()
        self.fields["date"].initial = timezone.now()


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = {
            "budgeted_amount",
            "category",
            "month",
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        month = cleaned_data.get("month")

        if not category or not month:
            self.add_error(
                None,
                ValidationError("A budget for this category and month already exists."),
            )
        return cleaned_data
