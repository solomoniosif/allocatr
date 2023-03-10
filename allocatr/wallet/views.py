import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, TemplateView
from django.views.decorators.http import require_POST

from .forms import ExpenseForm, IncomeForm, TransferForm
from .models import UserSettings, Account, Transaction


class DashboardHome(TemplateView):
    template_name = "wallet/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


def transactions(request):
    transactions = Transaction.objects.filter(account__user=request.user)
    context = {"transactions": transactions}
    return render(request, "wallet/partials/transactions.html", context)


def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    context = {"transaction": transaction}
    return render(request, "wallet/partials/transaction_detail.html", context)


def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "incomeCreated": None}
                    )
                },
            )
    else:
        form = IncomeForm()
    return render(request, "wallet/partials/add_income.html", {"form": form})


def add_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "expenseCreated": None}
                    )
                },
            )
    else:
        form = ExpenseForm()
    return render(request, "wallet/partials/add_expense.html", {"form": form})


def add_transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "transferCreated": None}
                    )
                },
            )
    else:
        form = TransferForm()
    return render(request, "wallet/partials/add_transfer.html", {"form": form})


def edit_income(request, pk):
    income = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "incomeEdited": None}
                    )
                },
            )
    else:
        form = IncomeForm(instance=income)
    return render(
        request,
        "wallet/partials/edit_income.html",
        {
            "form": form,
            "income": income,
        },
    )


def edit_expense(request, pk):
    expense = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "expenseEdited": None}
                    )
                },
            )
    else:
        form = ExpenseForm(instance=expense)
    return render(
        request,
        "wallet/partials/edit_expense.html",
        {
            "form": form,
            "expense": expense,
        },
    )


def edit_transfer(request, pk):
    transfer = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = TransferForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "transferEdited": None}
                    )
                },
            )
    else:
        form = TransferForm(instance=transfer)
    return render(
        request,
        "wallet/partials/edit_transfer.html",
        {
            "form": form,
            "transfer": transfer,
        },
    )


@require_POST
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    transaction.delete()
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {"transactionListChanged": None, "transactionDeleted": None}
            )
        },
    )


def account_cards(request):
    user_accounts = Account.objects.filter(user=request.user)
    user_settings = UserSettings.objects.get(user=request.user)
    wallet_balance = sum([account.current_balance for account in user_accounts])
    context = {
        "accounts": user_accounts,
        "currency": user_settings.currency,
        "wallet_balance": wallet_balance,
    }
    return render(request, "wallet/partials/accounts.html", context)


class Accounts(LoginRequiredMixin, ListView):
    model = Account
    template_name = "wallet/accounts.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = []
        for account in context["account_list"]:
            transactions = account.transactions.order_by('-created_at')[:5]
            accounts.append({"details": account, "transactions": transactions})
        context["accounts"] = accounts
        context['user_settings'] = UserSettings.objects.get(user=self.request.user)
        return context
