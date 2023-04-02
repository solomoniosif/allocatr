import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, ListView

from ..forms import BudgetForm
from ..models import Budget, Transaction
from ..services import get_or_create_month


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget
    context_object_name = "budgets"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return "wallet/budgets/partials/list.html"
        return "wallet/budgets/budget_list.html"


class BudgetDetailView(LoginRequiredMixin, DetailView):
    model = Budget
    context_object_name = "budget"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return "wallet/budgets/partials/detail.html"
        return "wallet/budgets/budget_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        if not self.object.is_master:
            transactions = Transaction.objects.filter(
                category=self.object.category,
                date__gte=month.first_day,
                date__lte=month.last_day,
            )
        else:
            transactions = Transaction.objects.filter(
                date__gte=month.first_day,
                date__lte=month.last_day,
            )
        context["transactions"] = transactions
        return context


class BudgetCreateView(LoginRequiredMixin, CreateView):
    model = Budget
    form_class = BudgetForm
    template_name = "wallet/budgets/partials/add_budget.html"
    context_object_name = "budget"
    success_url = None

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return HttpResponse(
            status=204,
            headers={
                "HX-Trigger": json.dumps(
                    {
                        "budget-created": None,
                        "budgets-changed": None,
                        "show-message": f"Budget {form.instance.name} created",
                    }
                )
            },
        )
