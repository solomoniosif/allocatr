import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from ..forms import ExpenseForm, IncomeForm, TransferForm
from ..htmx_views import (
    HtmxListView,
    HtmxOnlyCreateView,
    HtmxOnlyDeleteView,
    HtmxOnlyDetailView,
    HtmxOnlyListView,
    HtmxOnlyUpdateView,
)
from ..models import Transaction, UserSettings
from ..services import get_or_create_month


class TransactionListView(LoginRequiredMixin, HtmxListView):
    model = Transaction
    context_object_name = "transactions"
    htmx_template_name = "wallet/transactions/partials/list.html"
    template_name = "wallet/transactions/transaction_list.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        return qs.filter(
            account__user=self.request.user,
            date__gte=month.first_day,
            date__lte=month.last_day,
        ).prefetch_related("account", "category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        context["user_settings"] = user_settings
        return context


class TransactionPartialListView(LoginRequiredMixin, HtmxOnlyListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "wallet/transactions/partials/all_transactions_list_partial.html"

    def get_queryset(self):
        qs = super().get_queryset()
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        return qs.filter(
            account__user=self.request.user,
            date__gte=month.first_day,
            date__lte=month.last_day,
        )


class TransactionDetailView(LoginRequiredMixin, HtmxOnlyDetailView):
    model = Transaction
    context_object_name = "transaction"
    template_name = "wallet/transactions/partials/detail.html"


class IncomeCreateView(LoginRequiredMixin, HtmxOnlyCreateView):
    model = Transaction
    form_class = IncomeForm
    template_name = "wallet/transactions/partials/add_income.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        previous_income = Transaction.objects.income()
        income_titles = list(set([income.title for income in previous_income]))
        context["income_titles"] = income_titles
        return context

    def form_valid(self, form):
        self.object = form.save()  # noqa
        return HttpResponse(
            status=201,
            headers={
                "HX-Trigger": json.dumps(
                    {
                        "transactions-changed": None,
                        "income-created": None,
                        "show-message": f"Income {form.instance.title} added",
                    }
                )
            },
        )


class ExpenseCreateView(LoginRequiredMixin, HtmxOnlyCreateView):
    model = Transaction
    form_class = ExpenseForm
    template_name = "wallet/transactions/partials/add_expense.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        previous_expenses = Transaction.objects.expenses()
        expense_titles = list(set([expense.title for expense in previous_expenses]))
        context["expense_titles"] = expense_titles
        return context

    def form_valid(self, form):
        self.object = form.save()  # noqa
        return HttpResponse(
            status=201,
            headers={
                "HX-Trigger": json.dumps(
                    {
                        "transactions-changed": None,
                        "expense-created": None,
                        "show-message": f"Expense {form.instance.title} added",
                    }
                )
            },
        )


class TransferCreateView(LoginRequiredMixin, HtmxOnlyCreateView):
    model = Transaction
    form_class = TransferForm
    template_name = "wallet/transactions/partials/add_transfer.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        return HttpResponse(
            status=201,
            headers={
                "HX-Trigger": json.dumps(
                    {
                        "transactions-changed": None,
                        "transfer-created": None,
                        "show-message": f"Transfer {form.instance.title} added",
                    }
                )
            },
        )


class IncomeUpdateView(LoginRequiredMixin, HtmxOnlyUpdateView):
    model = Transaction
    form_class = IncomeForm
    context_object_name = "income"
    template_name = "wallet/transactions/partials/update_income.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "transactions-changed": None,
                    "income-edited": None,
                    "show-message": f"Income {form.instance.title} updated",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)


class ExpenseUpdateView(LoginRequiredMixin, HtmxOnlyUpdateView):
    model = Transaction
    form_class = ExpenseForm
    context_object_name = "expense"
    template_name = "wallet/transactions/partials/update_expense.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "transactions-changed": None,
                    "expense-edited": None,
                    "show-message": f"Expense {form.instance.title} updated",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)


class TransferUpdateView(LoginRequiredMixin, HtmxOnlyUpdateView):
    model = Transaction
    form_class = TransferForm
    context_object_name = "transfer"
    template_name = "wallet/transactions/partials/update_transfer.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "transactions-changed": None,
                    "transfer-edited": None,
                    "show-message": f"Transfer {form.instance.title} updated",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)


class TransactionDeleteView(LoginRequiredMixin, HtmxOnlyDeleteView):
    model = Transaction

    def form_valid(self, form):
        title = self.object.title
        self.object.delete()
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "transactions-changed": None,
                    "transaction-deleted": None,
                    "show-message": f"Transaction {title} deleted",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)
