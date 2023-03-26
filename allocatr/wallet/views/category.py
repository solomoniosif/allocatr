import json
from datetime import date

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from ..forms import CategoryForm
from ..mixins import RequirePostMixin
from ..models import Category, Transaction, UserSettings
from ..services import get_or_create_month


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        categories = {}
        for category in context["category_list"]:
            transactions = Transaction.objects.filter(
                category=category,
                date__gte=month.first_day,
                date__lte=month.last_day,
            )
            if category.group in categories:
                categories[category.group].append(
                    {
                        "details": category,
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

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return "wallet/categories/partials/list.html"
        return "wallet/categories/category_list.html"


class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = Category
    context_object_name = "category"

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

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return "wallet/categories/partials/detail.html"
        return "wallet/categories/category_detail.html"


class CategoryCreateView(LoginRequiredMixin, CreateView):
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

    def form_invalid(self, form):
        print("Form invalid")
        print(form.errors)
        super().form_invalid(form)
        return HttpResponse(
            form.errors,
            status=400,
        )


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    context_object_name = "category"
    template_name = "wallet/categories/partials/update_category.html"
    success_url = None

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


class CategoryDeleteView(LoginRequiredMixin, RequirePostMixin, DeleteView):
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
                    "show-message": f"Category {name}  deleted",
                }
            )
        }
        return HttpResponse(status=204, headers=headers)
