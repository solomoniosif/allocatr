from datetime import date
import json

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from django.db.models import Q

from .forms import ExpenseForm, IncomeForm, TransferForm
from .mixins import RequirePostMixin
from .models import UserSettings, Account, Transaction


class DashboardHome(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        context["user_settings"] = user_settings
        return context

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return "wallet/partials/dashboard_home_partial.html"
        return "wallet/dashboard_home.html"


def current_period(request):
    user_settings = UserSettings.objects.get(user=request.user)
    first_day, last_day = user_settings.get_current_period(date.today())
    period = {"firstDay": first_day.isoformat(), "lastDay": last_day.isoformat()}
    return JsonResponse(period, safe=False)


def previous_period(request, day: str):
    user_settings = UserSettings.objects.get(user=request.user)
    next_period_first_day = date.fromisoformat(day)
    first_day, last_day = user_settings.get_previous_period(next_period_first_day)
    period = {"firstDay": first_day.isoformat(), "lastDay": last_day.isoformat()}
    return JsonResponse(period, safe=False)


def next_period(request, day: str):
    user_settings = UserSettings.objects.get(user=request.user)
    previous_period_last_day = date.fromisoformat(day)
    first_day, last_day = user_settings.get_next_period(previous_period_last_day)
    period = {"firstDay": first_day.isoformat(), "lastDay": last_day.isoformat()}
    return JsonResponse(period, safe=False)


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "wallet/transactions/partials/transaction_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        first_period_day = self.request.GET["firstPeriodDay"]
        last_period_day = self.request.GET["lastPeriodDay"]
        return qs.filter(
            account__user=self.request.user,
            date__gte=first_period_day,
            date__lte=last_period_day,
        )


class TransactionDetailView(DetailView):
    model = Transaction
    context_object_name = "transaction"
    template_name = "wallet/transactions/partials/transaction_detail.html"


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = IncomeForm
    template_name = "wallet/transactions/partials/add_income.html"

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
    template_name = "wallet/transactions/partials/add_expense.html"

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
    template_name = "wallet/transactions/partials/add_transfer.html"

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
    template_name = "wallet/transactions/partials/edit_income.html"
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
    template_name = "wallet/transactions/partials/edit_expense.html"
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
    template_name = "wallet/transactions/partials/edit_transfer.html"
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
    template_name = "wallet/accounts/partials/account_cards.html"

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
    # template_name = "wallet/accounts/account_list.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accounts = []
        for account in context["account_list"]:
            transactions = Transaction.objects.filter(
                Q(account=account) | Q(to_account=account)
            )
            accounts.append({"details": account, "transactions": transactions})
        context["accounts"] = accounts
        context["user_settings"] = UserSettings.objects.get(user=self.request.user)
        return context

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return "wallet/accounts/partials/account_list_partial.html"
        return "wallet/accounts/dashboard_accounts.html"


class AccountDetailView(DetailView):
    model = Account
    context_object_name = "account"
    template_name = "wallet/accounts/account_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        accound_pk = context["account"].pkid

        all_tr = Transaction.objects.filter(
            Q(account=self.get_object()) | Q(to_account=self.get_object())
        )
        context["transactions"] = all_tr
        context["user_settings"] = UserSettings.objects.get(user=self.request.user)
        return context
