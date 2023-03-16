import uuid
from datetime import date
from colorfield.fields import ColorField

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db import models

from .utils import COLOR_PALETTE, get_month_range, is_color_dark

User = get_user_model()


class TimeStampedUUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at", "-updated_at"]


class UserSettings(models.Model):
    class Currency(models.TextChoices):
        AUD = "AUD", _("Australia Dollar")
        CAD = "CAD", _("Canada Dollar")
        CNY = "¥", _("China Yuan Renminbi")
        EUR = "€", _("Euro Member Countries")
        RON = "lei", _("Romania Leu")
        GBP = "£", _("United Kingdom Pound")
        USD = "$", _("United States Dollar")

    user = models.OneToOneField(User, related_name="settings", on_delete=models.CASCADE)
    currency = models.CharField(
        max_length=3, choices=Currency.choices, default=Currency.USD
    )
    start_day_of_month = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MaxValueValidator(28, message=_("Value must be between 1 and 28.")),
            MinValueValidator(1, message=_("Value must be between 1 and 28.")),
        ],
    )

    class Meta:
        verbose_name_plural = "User Settings"


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

    user = models.ForeignKey(
        User, verbose_name=_("User"), related_name="accounts", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name=_("Name"), max_length=50)
    account_type = models.CharField(
        verbose_name=_("Type"),
        max_length=2,
        choices=AccountType.choices,
        default=AccountType.GENERAL,
    )
    current_balance = models.DecimalField(
        verbose_name=_("Balance"), max_digits=10, decimal_places=2, default=0.0
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
    color = ColorField(
        verbose_name=_("Color on Dashboard"), samples=COLOR_PALETTE, default="#7DD181"
    )
    text_color = models.CharField(
        verbose_name=_("Text color"), max_length=12, blank=True, editable=False
    )

    def get_bg_color(self):
        tailwind_color = "red-500"
        for color in COLOR_PALETTE:
            if color[0] == self.color:
                tailwind_color = color[1]
        return f"bg-{tailwind_color}"

    class Meta:
        ordering = ["-active", "name"]
        unique_together = (("name", "account_type"),)

    def __str__(self):
        return f"{self.name.title()}"

    def save(self, *args, **kwargs):
        self.text_color = "white" if is_color_dark(self.color) else "black"
        super(Account, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("wallet:account_detail", kwargs={"pk": self.pk})


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
    color = ColorField(
        verbose_name=_("Color on Dashboard"), samples=COLOR_PALETTE, default="#7DD181"
    )
    text_color = models.CharField(
        verbose_name=_("Text color"), max_length=12, blank=True, editable=False
    )

    objects = models.Manager()
    income = IncomeManager()
    expense = ExpenseManager()
    transfer = TransferManager()

    class Meta:
        verbose_name_plural = _("Categories")
        ordering = ["group", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.text_color = "white" if is_color_dark(self.color) else "black"
        super(Category, self).save(*args, **kwargs)


class Transaction(TimeStampedUUIDModel):
    class TransactionType(models.TextChoices):
        INCOME = "IN", _("Income")
        EXPENSE = "EX", _("Expense")
        TRANSFER = "TR", _("Transfer")

    title = models.CharField(verbose_name=_("Title"), max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(default=date.today)
    transaction_type = models.CharField(
        verbose_name=_("Transaction type"),
        max_length=2,
        choices=TransactionType.choices,
    )
    account = models.ForeignKey(
        Account,
        verbose_name=_("Account"),
        related_name="transactions",
        on_delete=models.CASCADE,
    )
    to_account = models.ForeignKey(
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

    def get_absolute_url(self):
        return reverse("wallet:transaction-detail", kwargs={"pk": self.pk})

    def clean(self):
        if self.pkid is not None:
            pass
        elif (
            self.transaction_type
            in [self.TransactionType.EXPENSE, self.TransactionType.TRANSFER]
            and not self.account.balance_can_be_negative
            and self.account.current_balance < self.amount
        ):
            raise ValidationError(
                _("Transaction amount is higher than account balance!")
            )
        if (
            self.transaction_type == self.TransactionType.TRANSFER
            and not self.to_account
        ):
            raise ValidationError(
                _("For a transfer transaction a destination account must be specified!")
            )

    def save(self, *args, **kwargs):
        if self.transaction_type == self.TransactionType.INCOME:
            if self.pkid is not None:
                old_transaction = Transaction.objects.get(pk=self.pkid)
                old_transaction.account.current_balance -= old_transaction.amount
                old_transaction.account.save()
                self.account.refresh_from_db()
                self.account.current_balance += self.amount
            else:
                self.account.current_balance += self.amount
        elif self.transaction_type == self.TransactionType.EXPENSE:
            if self.pkid is not None:
                old_transaction = Transaction.objects.get(pk=self.pkid)
                old_transaction.account.current_balance += old_transaction.amount
                old_transaction.account.save()
                self.account.refresh_from_db()
                self.account.current_balance -= self.amount
            else:
                self.account.current_balance -= self.amount
        elif self.transaction_type == self.TransactionType.TRANSFER:
            if self.pkid is not None:
                old_transaction = Transaction.objects.get(pk=self.pkid)
                old_transaction.account.current_balance += old_transaction.amount
                old_transaction.to_account.current_balance -= old_transaction.amount
                old_transaction.account.save()
                old_transaction.to_account.save()
                self.account.refresh_from_db()
                self.to_account.refresh_from_db()
                self.account.current_balance -= self.amount
                self.to_account.current_balance += self.amount
                self.to_account.save()
            else:
                self.account.current_balance -= self.amount
                self.to_account.current_balance += self.amount
                self.to_account.save()
        self.account.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.transaction_type == self.TransactionType.INCOME:
            self.account.current_balance -= self.amount
        elif self.transaction_type == self.TransactionType.EXPENSE:
            self.account.current_balance += self.amount
        elif self.transaction_type == self.TransactionType.TRANSFER:
            self.account.current_balance += self.amount
            self.to_account.current_balance -= self.amount
            self.to_account.save()
        self.account.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.get_transaction_type_display()} » {self.title} » {self.amount}"

    def __hash__(self):
        return hash(self.pkid)

    def __eq__(self, other):
        return self.pkid == other.pkid

    def is_income(self):
        return self.transaction_type == self.TransactionType.INCOME

    def is_expense(self):
        return self.transaction_type == self.TransactionType.EXPENSE

    def is_transfer(self):
        return self.transaction_type == self.TransactionType.TRANSFER


class Budget(TimeStampedUUIDModel):
    user = models.ForeignKey(
        User, verbose_name=_("User"), related_name="budgets", on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name=_("Name"), max_length=150)
    budgeted_amount = models.DecimalField(
        verbose_name=_("Budgeted mount"), max_digits=10, decimal_places=2, default=0
    )
    actual_amount = models.DecimalField(
        verbose_name=_("Actual amount"), max_digits=10, decimal_places=2
    )
    start_date = models.DateField(verbose_name=_("Start date"))
    end_date = models.DateField(verbose_name=_("End date"))

    def __str__(self):
        return self.name


class BudgetItem(TimeStampedUUIDModel):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
