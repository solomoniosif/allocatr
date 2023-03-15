import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.views.decorators.http import require_POST

from .forms import ExpenseForm, IncomeForm, TransferForm
from .mixins import RequirePostMixin
from .models import UserSettings, Account, Transaction


class DashboardHome(LoginRequiredMixin, TemplateView):
    template_name = "wallet/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "wallet/partials/transactions/transaction_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(account__user=self.request.user)


class TransactionDetailView(DetailView):
    model = Transaction
    context_object_name = "transaction"
    template_name = "wallet/partials/transactions/transaction_detail.html"


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = IncomeForm
    template_name = "wallet/partials/transactions/add_income.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        return HttpResponse(
            status=204,
            headers={
                "HX-Trigger": json.dumps(
                    {"transactionListChanged": None, "incomeCreated": None}
                )
            },
        )


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = ExpenseForm
    template_name = "wallet/partials/transactions/add_expense.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        return HttpResponse(
            status=204,
            headers={
                "HX-Trigger": json.dumps(
                    {"transactionListChanged": None, "expenseCreated": None}
                )
            },
        )


class TransferCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransferForm
    template_name = "wallet/partials/transactions/add_transfer.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        return HttpResponse(
            status=204,
            headers={
                "HX-Trigger": json.dumps(
                    {"transactionListChanged": None, "transferCreated": None}
                )
            },
        )


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = IncomeForm
    context_object_name = "income"
    template_name = "wallet/partials/transactions/edit_income.html"
    success_url = None

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {"transactionListChanged": None, "incomeEdited": None}
            )
        }
        return HttpResponse(status=204, headers=headers)


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = ExpenseForm
    context_object_name = "expense"
    template_name = "wallet/partials/transactions/edit_expense.html"
    success_url = None

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {"transactionListChanged": None, "expenseEdited": None}
            )
        }
        return HttpResponse(status=204, headers=headers)


class TransferUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransferForm
    context_object_name = "transfer"
    template_name = "wallet/partials/transactions/edit_transfer.html"
    success_url = None

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {"transactionListChanged": None, "transferEdited": None}
            )
        }
        return HttpResponse(status=204, headers=headers)


class TransactionDeleteView(LoginRequiredMixin, RequirePostMixin, DeleteView):
    model = Transaction
    success_url = None

    def form_valid(self, form):
        self.object.delete()
        headers = {
            "HX-Trigger": json.dumps(
                {"transactionListChanged": None, "transactionDeleted": None}
            )
        }
        return HttpResponse(status=204, headers=headers)


class AccountPartialListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = "wallet/partials/accounts.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_accounts = Account.objects.filter(user=self.request.user)
        user_settings = UserSettings.objects.get(user=self.request.user)
        wallet_balance = sum([account.current_balance for account in user_accounts])
        context["accounts"] = user_accounts
        context["currency"] = user_settings.currency
        context["wallet_balance"] = wallet_balance
        return context


class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = "wallet/account_list.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = []
        for account in context["account_list"]:
            transactions = account.transactions.order_by("-created_at")[:5]
            accounts.append({"details": account, "transactions": transactions})
        context["accounts"] = accounts
        context["user_settings"] = UserSettings.objects.get(user=self.request.user)
        return context


class AccountDetailView(DetailView):
    model = Account
    context_object_name = "account"
    template_name = "wallet/account_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = context["account"].transactions.all()
        context["user_settings"] = UserSettings.objects.get(user=self.request.user)
        return context
