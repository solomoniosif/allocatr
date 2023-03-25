from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from ..models import Budget


class BudgetListView(LoginRequiredMixin, ListView):
    model = Budget

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user=self.request.user)
