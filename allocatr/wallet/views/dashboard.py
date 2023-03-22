from datetime import date

from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
)

from ..models import UserSettings


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


def current_period(request):
    user_settings = UserSettings.objects.get(user=request.user)
    first_day, last_day = user_settings.get_current_period(date.today())
    period = {"firstDay": first_day.isoformat(), "lastDay": last_day.isoformat()}
    return JsonResponse(period, safe=False)


def previous_period(request, day: str):
    user_settings = UserSettings.objects.get(user=request.user)
    next_period_first_day = date.fromisoformat(day)
    first_day, last_day = user_settings.get_previous_period(next_period_first_day)
    period = {"firstDay": first_day.isoformat(), "lastDay": last_day.isoformat()}
    return JsonResponse(period, safe=False)


def next_period(request, day: str):
    user_settings = UserSettings.objects.get(user=request.user)
    previous_period_last_day = date.fromisoformat(day)
    first_day, last_day = user_settings.get_next_period(previous_period_last_day)
    period = {"firstDay": first_day.isoformat(), "lastDay": last_day.isoformat()}
    return JsonResponse(period, safe=False)
