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
    path("transactions/", views.TransactionListView.as_view(), name="transactions"),
    path(
        "hx/transactions/",
        views.TransactionPartialListView.as_view(),
        name="transaction_list_partial",
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
        "transactions/<int:pk>/update-income/",
        views.IncomeUpdateView.as_view(),
        name="edit_income",
    ),
    path(
        "transactions/add-expense/",
        views.ExpenseCreateView.as_view(),
        name="add_expense",
    ),
    path(
        "transactions/<int:pk>/update-expense/",
        views.ExpenseUpdateView.as_view(),
        name="edit_expense",
    ),
    path(
        "transactions/add-transfer/",
        views.TransferCreateView.as_view(),
        name="add_transfer",
    ),
    path(
        "transactions/<int:pk>/update-transfer/",
        views.TransferUpdateView.as_view(),
        name="edit_transfer",
    ),
    path(
        "transactions/<int:pk>/delete/",
        views.TransactionDeleteView.as_view(),
        name="delete_transaction",
    ),
    # Planned Transaction Views
    path(
        "transactions/planned/",
        views.PlannedTransactionListView.as_view(),
        name="planned_transactions",
    ),
    path(
        "transactions/planned/<int:pk>/",
        views.PlannedTransactionDetailView.as_view(),
        name="planned_transaction_detail",
    ),
    path(
        "transactions/planned/expenses/add/",
        views.PlannedExpenseCreateView.as_view(),
        name="add_planned_expense",
    ),
    path(
        "transactions/planned/income/add/",
        views.PlannedIncomeCreateView.as_view(),
        name="add_planned_income",
    ),
    path(
        "transactions/planned/income/<int:pk>/update/",
        views.PlannedExpenseUpdateView.as_view(),
        name="edit_planned_income",
    ),
    path(
        "transactions/planned/expenses/<int:pk>/update/",
        views.PlannedExpenseUpdateView.as_view(),
        name="edit_planned_expense",
    ),
    path(
        "transactions/planned/<int:pk>/delete/",
        views.PlannedTransactionDeleteView.as_view(),
        name="delete_planned_transaction",
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
        "accounts/<int:pk>/update/",
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
        "categories/<int:pk>/update/",
        views.CategoryUpdateView.as_view(),
        name="edit_category",
    ),
    path(
        "categories/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="delete_category",
    ),
    # Budget Views
    path("budgets/", views.BudgetListView.as_view(), name="budgets"),
    path("budgets/<int:pk>/", views.BudgetDetailView.as_view(), name="budget_detail"),
    path("budgets/add/", views.BudgetCreateView.as_view(), name="add_budget"),
    path(
        "budgets/master-budget/",
        views.MasterBudgetPartialView.as_view(),
        name="master_budget_partial",
    ),
]
