from datetime import date

from common.models import TimeStampedUUIDModel
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _

from .account import Account
from .category import Category


class Transaction(TimeStampedUUIDModel):
    class TransactionType(models.TextChoices):
        INCOME = "IN", _("Income")
        EXPENSE = "EX", _("Expense")
        TRANSFER = "TR", _("Transfer")

    default_type = TransactionType.EXPENSE

    title = models.CharField(verbose_name=_("Title"), max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(default=date.today)
    transaction_type = models.CharField(
        verbose_name=_("Transaction type"),
        max_length=2,
        choices=TransactionType.choices,
        default=default_type,
    )
    account = models.ForeignKey(
        Account,
        verbose_name=_("Account"),
        related_name="transactions",
        on_delete=models.CASCADE,
    )
    dest_account = models.ForeignKey(
        Account,
        verbose_name=_("Transfer destination account"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    notes = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Category, verbose_name=_("Category"), on_delete=models.PROTECT
    )

    def clean(self):
        if (
            self.transaction_type
            in [self.TransactionType.EXPENSE, self.TransactionType.TRANSFER]
            and not self.account.balance_can_be_negative
            and self.account.balance < self.amount
        ):
            raise ValidationError(
                _("Transaction amount is higher than account balance!")
            )
        if (
            self.transaction_type == self.TransactionType.TRANSFER
            and not self.dest_account
        ):
            raise ValidationError(
                _("For a transfer transaction a destination account must be specified!")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.pkid:
            self.transaction_type = self.default_type
        if self.transaction_type == self.TransactionType.INCOME:
            self.account.balance += self.amount

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_transaction_type_display()} » {self.title} » {self.amount}{self.account.currency.code}"


class IncomeTransactionManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(transaction_type=Transaction.TransactionType.INCOME)
        )

    def create(self, **kwargs):
        kwargs.update({"transaction_type": Transaction.TransactionType.INCOME})
        return super().create(**kwargs)


class ExpenseTransactionManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(transaction_type=Transaction.TransactionType.EXPENSE)
        )

    def create(self, **kwargs):
        kwargs.update({"transaction_type": Transaction.TransactionType.EXPENSE})
        return super(IncomeTransactionManager, self).create(**kwargs)


class TransferTransactionManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(transaction_type=Transaction.TransactionType.TRANSFER)
        )

    def create(self, **kwargs):
        kwargs.update({"transaction_type": Transaction.TransactionType.TRANSFER})
        return super(IncomeTransactionManager, self).create(**kwargs)


class Income(Transaction):
    default_type = Transaction.TransactionType.INCOME
    objects = IncomeTransactionManager()

    class Meta:
        proxy = True


class Expense(Transaction):
    default_type = Transaction.TransactionType.EXPENSE
    onjects = ExpenseTransactionManager()

    class Meta:
        proxy = True


class Transfer(Transaction):
    default_type = Transaction.TransactionType.TRANSFER
    objects = TransferTransactionManager()

    class Meta:
        proxy = True
