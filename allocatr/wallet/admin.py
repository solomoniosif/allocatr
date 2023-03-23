from django.contrib import admin

from .models import Account, Budget, Category, Month, Transaction, UserSettings


@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "currency",
    )


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = ("user", "first_day", "last_day", "override_last_day")


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "user",
        "account_type",
        "current_balance",
        "active",
        "exclude_from_budget",
    )
    list_display_links = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "group")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("title", "transaction_type", "amount", "date", "account", "notes")
    list_display_links = ("title",)
    list_filter = ("transaction_type", "account")
    search_fields = ("title",)
    date_hierarchy = "date"


admin.site.register(Budget)
