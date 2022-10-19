from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "allocatr.core"
    verbose_name = _("Core")

    def ready(self):
        import allocatr.core.signals  # noqa F405
