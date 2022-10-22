from django import forms

from .models.transaction import Income


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ("title", "amount", "date", "account", "category", "notes")
