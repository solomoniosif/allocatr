import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from ..forms import PlannedExpenseForm, PlannedIncomeForm
from ..htmx_views import (
    HtmxListView,
    HtmxOnlyCreateView,
    HtmxOnlyDeleteView,
    HtmxOnlyDetailView,
    HtmxOnlyUpdateView,
)
from ..models import PlannedTransaction, UserSettings
from ..services import get_or_create_month


class PlannedTransactionListView(LoginRequiredMixin, HtmxListView):
    model = PlannedTransaction
    context_object_name = "planned_transactions"
    htmx_template_name = "wallet/planned_transactions/partials/list.html"
    template_name = "wallet/planned_transactions/plannedtransaction_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        return qs.filter(
            account__user=self.request.user,
            date__gte=month.first_day,
            date__lte=month.last_day,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        context["user_settings"] = user_settings
        return context


class PlannedTransactionDetailView(LoginRequiredMixin, HtmxOnlyDetailView):
    model = PlannedTransaction
    context_object_name = "planned_transaction"
    template_name = "wallet/planned_transactions/partials/detail.html"


class PlannedIncomeCreateView(LoginRequiredMixin, HtmxOnlyCreateView):
    model = PlannedTransaction
    form_class = PlannedIncomeForm
    template_name = "wallet/planned_transactions/partials/add_planned_income.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        title = form.instance.title
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "planned-transactions-changed": None,
                    "planned-income-created": None,
                    "show-message": f"Planned income {title} added",
                }
            )
        }
        return HttpResponse(status=201, headers=headers)


class PlannedExpenseCreateView(LoginRequiredMixin, HtmxOnlyCreateView):
    model = PlannedTransaction
    form_class = PlannedExpenseForm
    template_name = "wallet/planned_transactions/partials/add_planned_expense.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "planned-transactions-changed": None,
                    "planned-expense-created": None,
                    "show-message": f"Planned expense {form.instance.title} added",
                }
            )
        }
        return HttpResponse(status=201, headers=headers)


class PlannedIncomeUpdateView(LoginRequiredMixin, HtmxOnlyUpdateView):
    model = PlannedTransaction
    form_class = PlannedIncomeForm
    context_object_name = "planned_income"
    template_name = "wallet/planned_transactions/partials/update_planned_income.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "planed-transactions-changed": None,
                    "planned-income-updated": None,
                    "show-message": f"Planned income {form.instance.title} updated",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)


class PlannedExpenseUpdateView(LoginRequiredMixin, HtmxOnlyUpdateView):
    model = PlannedTransaction
    form_class = PlannedExpenseForm
    context_object_name = "planned_expense"
    template_name = "wallet/planned_transactions/partials/update_planned_expense.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "planned-transactions-changed": None,
                    "planned-expense-updated": None,
                    "show-message": f"Planned expense {form.instance.title} updated",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)


class PlannedTransactionDeleteView(LoginRequiredMixin, HtmxOnlyDeleteView):
    model = PlannedTransaction
    success_url = None

    def form_valid(self, form):
        title = self.object.title
        self.object.delete()
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "planned-transactions-changed": None,
                    "planned-transaction-deleted": None,
                    "show-message": f"Planned transaction {title} deleted",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)
