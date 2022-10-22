from django.shortcuts import render
from django.views.generic import CreateView, ListView

from .models.transaction import Income, Transaction


def dashboard_home(request):
    return render(request, "core/index.html")


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
