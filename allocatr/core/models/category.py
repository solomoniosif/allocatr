from common.models import TimeStampedUUIDModel
from django.db import models
from django.utils.translation import gettext as _


class IncomeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group="IN")


class ExpenseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group="EX")


class TransferManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group="TR")


class Category(TimeStampedUUIDModel):
    class Group(models.TextChoices):
        INCOME = "IN", _("Income")
        EXPENSE = "EX", _("Expense")
        TRANSFER = "TR", _("Transfer")

    group = models.CharField(
        verbose_name=_("Category group"),
        max_length=2,
        choices=Group.choices,
        default=Group.EXPENSE,
    )
    name = models.CharField(_("Name"), max_length=100)
    active = models.BooleanField(default=True)

    objects = models.Manager()
    income = IncomeManager()
    expense = ExpenseManager()
    transfer = TransferManager()

    class Meta:
        verbose_name_plural = _("Categories")
        ordering = ["group", "name"]

    def __str__(self):
        return self.name
