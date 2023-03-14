from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [
    # Home
    path("", views.DashboardHome.as_view(), name="home"),
    # Transaction Views
    path("htmx/transactions/", views.transactions, name="transaction_list"),
    path(
        "htmx/transaction/<int:pk>/",
        views.transaction_detail,
        name="transaction_detail",
    ),
    path("htmx/add-income/", views.IncomeCreateView.as_view(), name="add_income"),
    path("htmx/edit-income/<int:pk>/", views.edit_income, name="edit_income"),
    path("htmx/add-expense/", views.add_expense, name="add_expense"),
    path("htmx/edit-expense/<int:pk>/", views.edit_expense, name="edit_expense"),
    path("htmx/add-transfer/", views.add_transfer, name="add_transfer"),
    path("htmx/edit-transfer/<int:pk>/", views.edit_transfer, name="edit_transfer"),
    path(
        "htmx/delete-transaction/<int:pk>/",
        views.delete_transaction,
        name="delete_transaction",
    ),
    # Account Views
    path("wallet-accounts/", views.AccountListView.as_view(), name="accounts"),
    path("wallet-account/<int:pk>/", views.AccountDetailView.as_view(), name="account_detail"),
    path("htmx/accounts/", views.account_cards, name="accounts_list"),
]
