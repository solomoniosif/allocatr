from datetime import date
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

from ..forms import ExpenseForm, IncomeForm, TransferForm
from ..mixins import RequirePostMixin
from ..models import Transaction

from ..services import get_or_create_month


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "wallet/transactions/partials/transaction_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        day_or_month = self.request.GET.get("month")
        print(day_or_month)
        if not day_or_month:
            day_or_month = date.today()
        month = get_or_create_month(self.request.user, day_or_month)
        return qs.filter(
            account__user=self.request.user,
            date__gte=month.first_day,
            date__lte=month.last_day,
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
                    {
                        "transactions-changed": None,
                        "income-created": None,
                        "show-message": f"Income {form.instance.title.upper()} added successfully",
                    }
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
                    {
                        "transactions-changed": None,
                        "expense-created": None,
                        "show-message": f"Expense {form.instance.title.upper()} added successfully",
                    }
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
                    {
                        "transactions-changed": None,
                        "transfer-created": None,
                        "show-message": f"Transfer {form.instance.title.upper()} added successfully",
                    }
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
                {
                    "transactions-changed": None,
                    "income-edited": None,
                    "show-message": f"Income {form.instance.title.upper()} updated",
                }
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
                {
                    "transactions-changed": None,
                    "expense-edited": None,
                    "show-message": f"Expense {form.instance.title.upper()} updated",
                }
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
                {
                    "transactions-changed": None,
                    "transfer-edited": None,
                    "show-message": f"Transfer {form.instance.title.upper()} updated",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)


class TransactionDeleteView(LoginRequiredMixin, RequirePostMixin, DeleteView):
    model = Transaction
    success_url = None

    def form_valid(self, form):
        name = self.object.title
        self.object.delete()
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "transactions-changed": None,
                    "transaction-deleted": None,
                    "show-message": f"Transaction {name.upper()} deleted",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)
