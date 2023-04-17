import json
from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from ..htmx_views import HtmxTemplateView
from ..models import Transaction, UserSettings
from ..services import get_current_month_expenses, get_or_create_month

User = get_user_model()


class DashboardHome(LoginRequiredMixin, HtmxTemplateView):
    htmx_template_name = "wallet/home/partials/home.html"
    template_name = "wallet/home/dashboard_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        context["user_settings"] = user_settings
        day_or_month = self.request.GET.get("month", date.today())
        month = get_or_create_month(self.request.user, day_or_month)
        transactions = Transaction.objects.filter(
            account__user=self.request.user,
            date__gte=month.first_day,
            date__lte=month.last_day,
        ).prefetch_related("account", "category")
        context["transactions"] = transactions
        expense_data = get_current_month_expenses(self.request.user)
        context["monthDays"] = json.dumps(expense_data["monthDays"])
        context["actualExpenses"] = json.dumps(expense_data["actualExpenses"])
        context["plannedExpenses"] = json.dumps(expense_data["plannedExpenses"])
        return context


def get_current_month(request):
    current_month = get_or_create_month(request.user, date.today())
    response = {
        "firstDay": current_month.first_day.isoformat(),
        "lastDay": current_month.last_day.isoformat(),
        "month": current_month.month_code,
    }
    return JsonResponse(response, safe=False)


def get_previous_month(request, month: str):
    previous_month = get_or_create_month(request.user, month, -15)
    response = {
        "firstDay": previous_month.first_day.isoformat(),
        "lastDay": previous_month.last_day.isoformat(),
        "month": previous_month.month_code,
    }
    return JsonResponse(response, safe=False)


def get_next_month(request, month: str):
    next_month = get_or_create_month(request.user, month, 45)
    response = {
        "firstDay": next_month.first_day.isoformat(),
        "lastDay": next_month.last_day.isoformat(),
        "month": next_month.month_code,
    }
    return JsonResponse(response, safe=False)
