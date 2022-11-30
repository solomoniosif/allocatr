from django import forms
from django.utils import timezone

from .models.category import Category
from .models.transaction import Transaction


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("title", "amount", "date", "account", "category", "notes", "type")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        income_categories = Category.objects.filter(group=Category.Group.INCOME)
        self.fields["category"].queryset = income_categories
        self.fields["type"].initial = "IN"
        self.fields["type"].widget = forms.HiddenInput()
        self.fields["date"].initial = timezone.now()


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ("title", "amount", "date", "account", "category", "notes", "type")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        expense_categories = Category.objects.filter(group=Category.Group.EXPENSE)
        self.fields["category"].queryset = expense_categories
        self.fields["type"].initial = "EX"
        self.fields["type"].widget = forms.HiddenInput()
        self.fields["date"].initial = timezone.now()


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            "title",
            "amount",
            "date",
            "account",
            "dest_account",
            "category",
            "notes",
            "type",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        transfer_categories = Category.objects.filter(group=Category.Group.TRANSFER)
        self.fields["category"].queryset = transfer_categories
        self.fields["type"].initial = "EX"
        self.fields["type"].widget = forms.HiddenInput()
        self.fields["date"].initial = timezone.now()
        self.fields["account"].label = "Source account"
        self.fields["dest_account"].label = "Destination account"
