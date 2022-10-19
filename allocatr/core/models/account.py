from colorfield.fields import ColorField
from common.models import TimeStampedUUIDModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _

from .currency import Currency

User = get_user_model()


class Account(TimeStampedUUIDModel):
    class AccountType(models.TextChoices):
        GENERAL = "GA", _("General")
        CASH = "CA", _("Cash")
        CURRENT = "CU", _("Current")
        SAVINGS = "SA", _("Savings")
        INSURANCE = "IS", _("Insurance")
        INVESTMENT = "IV", _("Investment")
        CREDIT_CARD = "CC", _("Credit Card")
        LOAN = "LO", _("Loan")

    COLOR_PALETTE = [
        # Greens
        ("#7DD181", "Mantis"),
        ("#16DB65", "Malachite"),
        ("#51CB20", "Lime Green"),
        ("#BDD358", "June Bud"),
        ("#68A357", "Asparagus"),
        ("#32965D", "Green Cyan"),
        ("#09814A", "Sea Green"),
        ("#317B22", "Ao English"),
        # Reds
        ("#F1A7A9", "Pastel Pink"),
        ("#EC8385", "Light Coral"),
        ("#E66063", "Fuzzy Wuzzy"),
        ("#E35053", "Indian Red"),
        ("#FF3C38", "Tart Orange"),
        ("#E3170A", "Vermilion"),
        ("#BD1F21", "Firebrick"),
        ("#9C191B", "Ruby Red"),
        ("#F95738", "Orange Soda"),
        ("#D34E24", "Sinopia"),
        ("#EC9A29", "Carrot Orange"),
        ("#FF8C42", "Mango Tango"),
        ("#EE6352", "Fire Opal"),
        ("#F56476", "Fiery Rose"),
        ("#E87461", "Terra Cotta"),
        ("#E5C687", "Gold Crayola"),
        ("#FAC9B8", "Apricot"),
        ("#A1E8CC", "Magic Mint"),
        ("#41E2BA", "Medium Aquamarine"),
        ("#0F8B8D", "Dark Cyan"),
        ("#85C7F2", "Light Sky Blue"),
        ("#A1B5D8", "Wild Blue Yonder"),
        ("#805D93", "French Lilac"),
        ("#6F73D2", "Violet Blue Crayola"),
    ]

    user = models.ForeignKey(
        User, verbose_name=_("User"), related_name="accounts", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    account_type = models.CharField(
        verbose_name=_("Account Type"),
        max_length=2,
        choices=AccountType.choices,
        default=AccountType.GENERAL,
    )
    balance = models.DecimalField(
        verbose_name=_("Balance"), max_digits=10, decimal_places=2
    )
    currency = models.ForeignKey(
        Currency, verbose_name=_("Currency"), on_delete=models.PROTECT
    )
    balance_can_be_negative = models.BooleanField(
        verbose_name=_("Balance can be negative"), default=False
    )
    active = models.BooleanField(verbose_name=_("Active"), default=True)
    exclude_from_budget = models.BooleanField(
        verbose_name=_("Exclude from budget"), default=False
    )
    show_on_dashboard = models.BooleanField(
        verbose_name=_("Show on Dashboard"), default=True
    )
    color_on_dashboard = ColorField(
        verbose_name=_("Color on Dashboard"), samples=COLOR_PALETTE, default="#7DD181"
    )

    class Meta:
        ordering = ["-active", "name"]
        unique_together = (("name", "account_type"),)

    def __str__(self):
        return f"{self.name.title()} » {self.balance} {self.currency.code}"
