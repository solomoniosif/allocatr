from django.views.generic import CreateView, ListView, TemplateView

from .models.transaction import Income, Transaction


class DashboardHome(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TransactionListView(ListView):
    model = Transaction
    context_object_name = "transactions"
    template_name = "core/partials/_transaction_list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        user_transactions = qs.filter(account__user=self.request.user)
        return user_transactions


class IncomeCreateView(CreateView):
    model = Income
    template_name = "core/partials/_transaction_form.html"
