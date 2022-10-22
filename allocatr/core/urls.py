from django.urls import path

from allocatr.core import views

app_name = "core"
urlpatterns = [
    path("", views.DashboardHome.as_view(), name="home"),
]

htmx_urlpatterns = [
    path(
        "htmx-transactions-list/",
        views.TransactionListView.as_view(),
        name="transaction_list",
    ),
    path("htmx-income-create/", views.IncomeCreateView.as_view(), name="income_create"),
]
urlpatterns += htmx_urlpatterns
