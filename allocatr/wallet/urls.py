from django.urls import path

from . import views

app_name = "wallet"

urlpatterns = [
    # Home
    path("", views.DashboardHome.as_view(), name="home"),
    path("current-month/", views.get_current_month, name="current_month"),
    path(
        "previous-month/<str:month>/", views.get_previous_month, name="previous_month"
    ),
    path("next-month/<str:month>/", views.get_next_month, name="next_month"),
    # Transaction Views
    path(
        "transactions/",
        views.TransactionListView.as_view(),
        name="transaction_list",
    ),
    path(
        "transactions/<int:pk>/",
        views.TransactionDetailView.as_view(),
        name="transaction_detail",
    ),
    path(
        "transactions/add-income/", views.IncomeCreateView.as_view(), name="add_income"
    ),
    path(
        "transactions/<int:pk>/edit-income/",
        views.IncomeUpdateView.as_view(),
        name="edit_income",
    ),
    path(
        "transactions/add-expense/",
        views.ExpenseCreateView.as_view(),
        name="add_expense",
    ),
    path(
        "transactions/<int:pk>/edit-expense/",
        views.ExpenseUpdateView.as_view(),
        name="edit_expense",
    ),
    path(
        "transactions/add-transfer/",
        views.TransferCreateView.as_view(),
        name="add_transfer",
    ),
    path(
        "transactions/<int:pk>/edit-transfer/",
        views.TransferUpdateView.as_view(),
        name="edit_transfer",
    ),
    path(
        "transactions/<int:pk>/delete/",
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
        "accounts/partial/",
        views.AccountPartialListView.as_view(),
        name="accounts_list",
    ),
    path("accounts/add/", views.AccountCreateView.as_view(), name="add_account"),
    path(
        "accounts/<int:pk>/edit/",
        views.AccountUpdateView.as_view(),
        name="edit_account",
    ),
    path(
        "accounts/<int:pk>/delete/",
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
    path("categories/add/", views.CategoryCreateView.as_view(), name="add_category"),
    path(
        "categories/<int:pk>/edit/",
        views.CategoryUpdateView.as_view(),
        name="edit_category",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="delete_category",
    ),
]
