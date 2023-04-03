import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from ..forms import BudgetForm
from ..htmx_views import (
    HtmxDetailView,
    HtmxListView,
    HtmxOnlyCreateView,
    HtmxOnlyTemplateView,
)
from ..models import Budget, Transaction
from ..services import get_or_create_month


class BudgetListView(LoginRequiredMixin, HtmxListView):
    model = Budget
    context_object_name = "budgets"
    htmx_template_name = "wallet/budgets/partials/list.html"
    template_name = "wallet/budgets/budget_list.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        return qs.filter(user=self.request.user, month=month)


class BudgetDetailView(LoginRequiredMixin, HtmxDetailView):
    model = Budget
    context_object_name = "budget"
    htmx_template_name = "wallet/budgets/partials/detail.html"
    template_name = "wallet/budgets/budget_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        if not self.object.is_master:
            transactions = Transaction.objects.filter(
                account__user=self.request.user,
                category=self.object.category,
                date__gte=month.first_day,
                date__lte=month.last_day,
            )
        else:
            transactions = Transaction.objects.filter(
                account__user=self.request.user,
                date__gte=month.first_day,
                date__lte=month.last_day,
            )
        context["transactions"] = transactions
        return context


class MasterBudgetPartialView(LoginRequiredMixin, HtmxOnlyTemplateView):
    template_name = "wallet/budgets/partials/master_budget_partial.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        master_budget, _ = Budget.objects.get_or_create(
            user=self.request.user, is_master=True, month=month
        )
        context["master_budget"] = master_budget
        return context


class BudgetCreateView(LoginRequiredMixin, HtmxOnlyCreateView):
    form_class = BudgetForm
    template_name = "wallet/budgets/partials/add_budget.html"
    success_url = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "budget-created": None,
                    "budgets-changed": None,
                    "show-message": f"Budget {form.instance.name} created",
                }
            )
        }

        return HttpResponse(status=204, headers=headers)
