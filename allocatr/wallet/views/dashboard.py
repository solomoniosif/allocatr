from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import (
    TemplateView,
)

from ..models import Month, UserSettings


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


# def current_period(request):
#     user_settings = UserSettings.objects.get(user=request.user)
#     first_day, last_day = user_settings.get_current_period(date.today())
#     period = {"firstDay": first_day.isoformat(), "lastDay": last_day.isoformat()}
#     return JsonResponse(period, safe=False)


# def previous_period(request, day: str):
#     user_settings = UserSettings.objects.get(user=request.user)
#     next_period_first_day = date.fromisoformat(day)
#     first_day, last_day = user_settings.get_previous_period(next_period_first_day)
#     period = {"firstDay": first_day.isoformat(), "lastDay": last_day.isoformat()}
#     return JsonResponse(period, safe=False)


# def next_period(request, day: str):
#     user_settings = UserSettings.objects.get(user=request.user)
#     previous_period_last_day = date.fromisoformat(day)
#     first_day, last_day = user_settings.get_next_period(previous_period_last_day)
#     period = {"firstDay": first_day.isoformat(), "lastDay": last_day.isoformat()}
#     return JsonResponse(period, safe=False)


def get_or_create_month(user: User, day: date):
    start_day_of_month = user.settings.start_day_of_month
    if start_day_of_month <= day.day:
        first_day = date(day.year, day.month, start_day_of_month)
    else:
        first_day = date(day.year, day.month, start_day_of_month) - relativedelta(
            months=1
        )
    current_month, _ = Month.objects.get_or_create(user=user, first_day=first_day)
    return current_month


def get_current_month(request):
    current_month = get_or_create_month(request.user, date.today())
    response = {
        "firstDay": current_month.first_day.isoformat(),
        "lastDay": current_month.last_day.isoformat(),
        "month": current_month.month_code,
    }
    return JsonResponse(response, safe=False)


def get_previous_month(request, month: str):
    start_DOM = str(request.user.settings.start_day_of_month)
    date_str = f"{start_DOM.rjust(2, '0')}/{month[-2:]}/{month[:2]}"
    current_month_first_day = datetime.strptime(date_str, "%d/%m/%y").date()
    day_minus_15 = current_month_first_day - timedelta(days=15)
    previous_month = get_or_create_month(request.user, day_minus_15)
    response = {
        "firstDay": previous_month.first_day.isoformat(),
        "lastDay": previous_month.last_day.isoformat(),
        "month": previous_month.month_code,
    }
    return JsonResponse(response, safe=False)


def get_next_month(request, month: str):
    start_DOM = str(request.user.settings.start_day_of_month)
    date_str = f"{start_DOM.rjust(2, '0')}/{month[-2:]}/{month[:2]}"
    current_month_first_day = datetime.strptime(date_str, "%d/%m/%y").date()
    day_plus_45 = current_month_first_day + timedelta(days=45)
    next_month = get_or_create_month(request.user, day_plus_45)
    response = {
        "firstDay": next_month.first_day.isoformat(),
        "lastDay": next_month.last_day.isoformat(),
        "month": next_month.month_code,
    }
    return JsonResponse(response, safe=False)
