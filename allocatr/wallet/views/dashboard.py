from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import TemplateView

from ..models import UserSettings
from ..services import get_or_create_month

User = get_user_model()


class DashboardHome(LoginRequiredMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_settings = UserSettings.objects.get(user=self.request.user)
        context["user_settings"] = user_settings
        return context

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return "wallet/partials/dashboard_home_partial.html"
        return "wallet/dashboard_home.html"


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
