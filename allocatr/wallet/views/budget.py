import json
from datetime import date
from itertools import chain

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from ..forms import BudgetForm
from ..htmx_views import (
    HtmxDetailView,
    HtmxListView,
    HtmxOnlyCreateView,
    HtmxOnlyTemplateView,
    HtmxOnlyUpdateView,
)
from ..models import Budget, Category, PlannedTransaction, Transaction
from ..services import (
    get_master_budget_stats,
    get_or_create_month,
    get_or_create_next_13_months,
)


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
        master_budget_stats = get_master_budget_stats(month)
        master_budget, _ = Budget.objects.get_or_create(
            user=self.request.user, is_master=True, month=month
        )
        transactions = Transaction.objects.filter(
            account__user=self.request.user,
            date__gte=month.first_day,
            date__lte=month.last_day,
        )
        planned_transactions = PlannedTransaction.objects.filter(
            account__user=self.request.user,
            date__gte=month.first_day,
            date__lte=month.last_day,
        )
        all_transactions = list(chain(transactions, planned_transactions))
        ex_list = [
            {"value": int(tr.amount), "name": tr.title}
            for tr in all_transactions
            if tr.transaction_type == "EX"
        ]
        allocated_amount = sum([ex["value"] for ex in ex_list])
        unallocated_amount = int(master_budget.budgeted_amount) - allocated_amount
        budget = ex_list + [{"value": unallocated_amount, "name": "Unallocated"}]

        context["master_budget"] = master_budget
        context["transactions"] = all_transactions
        context["budget"] = json.dumps(budget)
        context["budget_stats"] = master_budget_stats
        return context


class BudgetCreateView(LoginRequiredMixin, HtmxOnlyCreateView):
    form_class = BudgetForm
    template_name = "wallet/budgets/partials/add_budget.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_13_months = get_or_create_next_13_months(self.request.user)
        months_list = [{"id": m.id, "name": m.__str__()} for m in next_13_months]
        context["month_list"] = json.dumps(months_list)
        return context

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


class CategoryBudgetCreateView(LoginRequiredMixin, HtmxOnlyCreateView):
    form_class = BudgetForm
    template_name = "wallet/budgets/partials/add_category_budget.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs["category_id"]
        category = Category.objects.get(pkid=category_id)
        next_13_months = get_or_create_next_13_months(self.request.user)
        months_list = [{"id": m.id, "name": m.__str__()} for m in next_13_months]
        context["category"] = category
        context["month_list"] = json.dumps(months_list)
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        category_id = self.kwargs["category_id"]
        category = Category.objects.get(pkid=category_id)
        form.instance.category = category
        self.object = form.save()
        message = f"{form.instance.month} budget for {category.name} created"
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "budget-created": None,
                    "budgets-changed": None,
                    "show-message": message,
                }
            )
        }

        return HttpResponse(status=204, headers=headers)


class BudgetUpdateView(LoginRequiredMixin, HtmxOnlyUpdateView):
    model = Budget
    form_class = BudgetForm
    template_name = "wallet/budgets/partials/update_budget.html"
    context_object_name = "budget"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        next_13_months = get_or_create_next_13_months(self.request.user)
        month_list = [{"id": m.id, "name": m.__str__()} for m in next_13_months]
        context["month_list"] = json.dumps(month_list)
        return context

    def form_valid(self, form):
        self.object = form.save()
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "budget-updated": None,
                    "budgets-changed": None,
                    "show-message": f"Budget {form.instance.name} updated",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)
