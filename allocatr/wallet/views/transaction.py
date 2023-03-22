import json

from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.db.models import Q

from ..forms import ExpenseForm, IncomeForm, TransferForm
from ..mixins import RequirePostMixin
from ..models import Transaction


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


class TransactionDetailView(LoginRequiredMixin, DetailView):
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
