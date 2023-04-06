import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse

from ..forms import CategoryForm
from ..htmx_views import (
    HtmxListView,
    HtmxOnlyCreateView,
    HtmxOnlyDeleteView,
    HtmxOnlyDetailView,
    HtmxOnlyUpdateView,
)
from ..models import Category, Transaction, UserSettings
from ..services import get_or_create_month


class CategoryListView(LoginRequiredMixin, HtmxListView):
    model = Category
    htmx_template_name = "wallet/categories/partials/list.html"
    template_name = "wallet/categories/category_list.html"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        categories = {}
        main_categories = self.get_queryset().filter(parent=None)
        for category in main_categories:
            transactions = Transaction.objects.filter(
                category=category,
                date__gte=month.first_day,
                date__lte=month.last_day,
            )
            if category.group in categories:
                categories[category.group].append(
                    {
                        "details": category,
                        "subcategories": category.subcategories.all(),
                        "transactions": transactions,
                        "transactions_count": transactions.count(),
                        "total_amount": transactions.aggregate(Sum("amount")),
                    }
                )
            else:
                categories[category.group] = [
                    {"details": category, "transactions": transactions}
                ]
        context["categories"] = categories
        context["user_settings"] = user_settings
        return context


class CategoryDetailView(LoginRequiredMixin, HtmxOnlyDetailView):
    model = Category
    context_object_name = "category"
    template_name = "wallet/categories/partials/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        filtered_transactions = Transaction.objects.filter(
            category=self.get_object(),
            date__gte=month.first_day,
            date__lte=month.last_day,
        )
        context["transactions"] = filtered_transactions
        context["amount_total"] = filtered_transactions.aggregate(Sum("amount"))
        context["transaction_names"] = [tr.title for tr in filtered_transactions]
        context["amounts"] = [int(tr.amount) for tr in filtered_transactions]
        context["user_settings"] = user_settings
        return context


class CategoryCreateView(LoginRequiredMixin, HtmxOnlyCreateView):
    model = Category
    form_class = CategoryForm
    template_name = "wallet/categories/partials/add_category.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return HttpResponse(
            status=204,
            headers={
                "HX-Trigger": json.dumps(
                    {
                        "category-created": None,
                        "categories-changed": None,
                        "show-message": f"Category {form.instance.name}  created",
                    }
                )
            },
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_categories = [
            {"id": c.pkid, "name": c.name, "group": c.group.upper()}
            for c in Category.objects.filter(user=self.request.user)
        ]
        context["categories"] = json.dumps(user_categories)
        return context


class CategoryUpdateView(LoginRequiredMixin, HtmxOnlyUpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "wallet/categories/partials/update_category.html"

    def form_valid(self, form):
        self.object = form.save()  # noqa
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "category-edited": None,
                    "categories-changed": None,
                    "show-message": f"Category {form.instance.name}  updated",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_categories = [
            {"id": c.pkid, "name": c.name, "group": c.group.upper()}
            for c in Category.objects.filter(user=self.request.user)
        ]
        context["categories"] = json.dumps(user_categories)
        return context


class CategoryDeleteView(LoginRequiredMixin, HtmxOnlyDeleteView):
    model = Category
    success_url = None

    def form_valid(self, form):
        name = self.object.name
        self.object.delete()
        headers = {
            "HX-Trigger": json.dumps(
                {
                    "category-deleted": None,
                    "categories-changed": None,
                    "show-message": f"Category {name} deleted",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)
