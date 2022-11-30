import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .forms import ExpenseForm, IncomeForm, TransferForm
from .models.transaction import Transaction


def transaction_list(request):
    transactions = Transaction.objects.filter(account__user=request.user)
    context = {"transactions": transactions}
    return render(request, "core/partials/transaction/_transaction_list.html", context)


def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    context = {"transaction": transaction}
    return render(
        request, "core/partials/transaction/_transaction_detail.html", context
    )


def create_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "incomeCreated": None}
                    )
                },
            )
    else:
        form = IncomeForm()
    return render(request, "core/partials/transaction/_income_add.html", {"form": form})


def edit_income(request, pk):
    income = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "incomeEdited": None}
                    )
                },
            )
    else:
        form = IncomeForm(instance=income)
    return render(
        request,
        "core/partials/transaction/_income_edit.html",
        {
            "form": form,
            "income": income,
        },
    )


@require_POST
def delete_transaction(request, pk):
    income = get_object_or_404(Transaction, pk=pk)
    income.delete()
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps(
                {"transactionListChanged": None, "transactionDeleted": None}
            )
        },
    )


def create_expense(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "expenseCreated": None}
                    )
                },
            )
    else:
        form = ExpenseForm()
    return render(
        request, "core/partials/transaction/_expense_add.html", {"form": form}
    )


def edit_expense(request, pk):
    expense = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "expenseEdited": None}
                    )
                },
            )
    else:
        form = ExpenseForm(instance=expense)
    return render(
        request,
        "core/partials/transaction/_expense_edit.html",
        {
            "form": form,
            "expense": expense,
        },
    )


def create_transfer(request):
    if request.method == "POST":
        form = TransferForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "transferCreated": None}
                    )
                },
            )
    else:
        form = TransferForm()
    return render(
        request, "core/partials/transaction/_transfer_add.html", {"form": form}
    )


def edit_transfer(request, pk):
    transfer = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = TransferForm(request.POST, instance=transfer)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"transactionListChanged": None, "transferEdited": None}
                    )
                },
            )
    else:
        form = TransferForm(instance=transfer)
    return render(
        request,
        "core/partials/transaction/_transfer_edit.html",
        {
            "form": form,
            "transfer": transfer,
        },
    )
