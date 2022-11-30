from django.urls import path

from allocatr.core import htmx_views, views

app_name = "core"
urlpatterns = [
    path("", views.DashboardHome.as_view(), name="home"),
]

htmx_urlpatterns = [
    path("htmx/transactions/", htmx_views.transaction_list, name="transaction_list"),
    path(
        "htmx/transaction-details/<int:pk>/",
        htmx_views.transaction_detail,
        name="transaction_detail",
    ),
    path(
        "htmx/delete-transaction/<int:pk>/",
        htmx_views.delete_transaction,
        name="delete_transaction",
    ),
    path("htmx/add-income/", htmx_views.create_income, name="add_income"),
    path("htmx/edit-income/<int:pk>/", htmx_views.edit_income, name="edit_income"),
    path("htmx/add-expense/", htmx_views.create_expense, name="add_expense"),
    path("htmx/edit-expense/<int:pk>/", htmx_views.edit_expense, name="edit_expense"),
    path("htmx/add-transfer/", htmx_views.create_transfer, name="add_transfer"),
    path(
        "htmx/edit-transfer/<int:pk>/", htmx_views.edit_transfer, name="edit_transfer"
    ),
]
urlpatterns += htmx_urlpatterns
