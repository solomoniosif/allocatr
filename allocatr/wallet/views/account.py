import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..forms import AccountForm
from ..mixins import RequirePostMixin
from ..models import Account, Transaction, UserSettings
from ..services import get_or_create_month


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

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        accounts = []
        for account in context["account_list"]:
            transactions = Transaction.objects.filter(
                Q(account=account) | Q(to_account=account),
                date__gte=month.first_day,
                date__lte=month.last_day,
            )
            accounts.append({"details": account, "transactions": transactions})
        context["accounts"] = accounts
        context["user_settings"] = user_settings
        return context

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return "wallet/accounts/partials/list.html"
        return "wallet/accounts/account_list.html"


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    context_object_name = "account"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        filtered_transactions = Transaction.objects.filter(
            Q(account=self.get_object()) | Q(to_account=self.get_object()),
            date__gte=month.first_day,
            date__lte=month.last_day,
        )
        context["transactions"] = filtered_transactions
        income_amounts = []
        expenses_amounts = []
        income = []
        expenses = []
        income_colors = []
        expense_colors = []
        for tr in filtered_transactions.order_by("-created_at"):
            if tr.transaction_type == Transaction.TransactionType.EXPENSE or (
                tr.transaction_type == Transaction.TransactionType.TRANSFER
                and tr.account == context["account"]
            ):
                expenses_amounts.append(int(tr.amount))
                expenses.append(tr.title)
                expense_colors.append(tr.category.color)
            elif tr.transaction_type == Transaction.TransactionType.INCOME:
                income_amounts.append(int(tr.amount))
                income.append(tr.title)
                income_colors.append(tr.category.color)
        context["expenses"] = expenses
        context["expenses_amounts"] = expenses_amounts
        context["expense_colors"] = expense_colors
        context["expense_total"] = sum(expenses_amounts)
        context["income"] = income
        context["income_amounts"] = income_amounts
        context["income_colors"] = income_colors
        context["income_total"] = sum(income_amounts)
        context["user_settings"] = user_settings
        return context

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return "wallet/accounts/partials/detail.html"
        return "wallet/accounts/account_detail.html"


class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = "wallet/accounts/partials/add_account.html"
    context_object_name = "account"
    success_url = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return HttpResponse(
            status=204,
            headers={
                "HX-Trigger": json.dumps(
                    {
                        "account-created": None,
                        "accounts-changed": None,
                        "show-message": f"Account {form.instance.name} created",
                    }
                )
            },
        )


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    context_object_name = "account"
    template_name = "wallet/accounts/partials/update_account.html"
    success_url = None

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "account-edited": None,
                    "accounts-changed": None,
                    "show-message": f"Account {form.instance.name} updated",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)


class AccountDeleteView(LoginRequiredMixin, RequirePostMixin, DeleteView):
    model = Account
    success_url = None

    def form_valid(self, form):
        name = self.object.name
        self.object.delete()
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "account-deleted": None,
                    "accounts-changed": None,
                    "show-message": f"{name} deleted",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)
