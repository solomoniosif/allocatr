from django.db import models
from django.utils.translation import gettext as _


class Currency(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    symbol = models.CharField(_("Symbol"), max_length=5)
    code = models.CharField(_("Code"), max_length=3)

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return self.code.upper()
