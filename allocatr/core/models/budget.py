from common.models import TimeStampedUUIDModel
from django.db import models
from django.utils.translation import gettext as _

from . import Category


class Budget(TimeStampedUUIDModel):
    class Period(models.TextChoices):
        WEEK = "WE", _("Week")
        MONTH = "MN", _("Month")
        YEAR = "YR", _("Year")

    category = models.ForeignKey(
        Category, verbose_name=_("Budget category"), on_delete=models.CASCADE
    )
    period = models.CharField(
        verbose_name=_("Period"),
        max_length=2,
        choices=Period.choices,
        default=Period.MONTH,
    )
    start_day = models.DateField(verbose_name=_("Start day"))
    end_day = models.DateField(verbose_name=_("End day"))
    amount = models.DecimalField(
        verbose_name=_("Amount"), max_digits=10, decimal_places=2, default=0
    )

    def __str__(self):
        return f"{self.get_period_display()}ly budget for {self.category.name}"
