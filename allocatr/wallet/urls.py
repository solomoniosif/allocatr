from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [
    # Home
    path("", views.DashboardHome.as_view(), name="home"),
    path("current-period/", views.current_period, name="current_period"),
    path("previous-period/<str:day>/", views.previous_period, name="previous_period"),
    path("next-period/<str:day>/", views.next_period, name="next_period"),
    # Transaction Views
    path(
        "htmx/transactions/",
        views.TransactionListView.as_view(),
        name="transaction_list",
    ),
    path(
        "htmx/transaction/<int:pk>/",
        views.TransactionDetailView.as_view(),
        name="transaction_detail",
    ),
    path("htmx/add-income/", views.IncomeCreateView.as_view(), name="add_income"),
    path(
        "htmx/edit-income/<int:pk>/",
        views.IncomeUpdateView.as_view(),
        name="edit_income",
    ),
    path("htmx/add-expense/", views.ExpenseCreateView.as_view(), name="add_expense"),
    path(
        "htmx/edit-expense/<int:pk>/",
        views.ExpenseUpdateView.as_view(),
        name="edit_expense",
    ),
    path("htmx/add-transfer/", views.TransferCreateView.as_view(), name="add_transfer"),
    path(
        "htmx/edit-transfer/<int:pk>/",
        views.TransferUpdateView.as_view(),
        name="edit_transfer",
    ),
    path(
        "htmx/delete-transaction/<int:pk>/",
        views.TransactionDeleteView.as_view(),
        name="delete_transaction",
    ),
    # Account Views
    path("accounts/", views.AccountListView.as_view(), name="accounts"),
    path(
        "accounts/<int:pk>/",
        views.AccountDetailView.as_view(),
        name="account_detail",
    ),
    path(
        "htmx/accounts/", views.AccountPartialListView.as_view(), name="accounts_list"
    ),
    path("htmx/add-account/", views.AccountCreateView.as_view(), name="add_account"),
    path(
        "htmx/edit-account/<int:pk>",
        views.AccountUpdateView.as_view(),
        name="edit_account",
    ),
    path(
        "htmx/delete-account/<int:pk>",
        views.AccountDeleteView.as_view(),
        name="delete_account",
    ),
    # Category Views
    path("categories/", views.CategoryListView.as_view(), name="categories"),
    path(
        "categories/<int:pk>/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path("htmx/add-category/", views.CategoryCreateView.as_view(), name="add_category"),
    path(
        "htmx/edit-category/<int:pk>/",
        views.CategoryUpdateView.as_view(),
        name="edit_category",
    ),
    path(
        "htmx/delete-account/<int:pk>/",
        views.CategoryDeleteView.as_view(),
        name="delete_category",
    ),
]
