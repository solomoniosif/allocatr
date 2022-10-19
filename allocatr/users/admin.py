from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    add_form = UserAdminCreationForm
    form = UserAdminChangeForm
    model = User
    list_display = [
        "get_full_name",
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_superuser",
    ]
    list_display_links = ["get_full_name", "email"]
    list_filter = ["email", "username", "first_name", "last_name", "is_staff"]
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            _("Personal Information"),
            {"fields": ("username", "first_name", "last_name")},
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ["email", "username", "first_name", "last_name"]
