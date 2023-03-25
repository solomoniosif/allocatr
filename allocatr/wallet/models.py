import uuid
from datetime import date, datetime, timedelta

from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _

from .querysets import AccountQuerySet, CategoryQuerySet, TransactionQuerySet
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
        CNY = "RMB", _("China Yuan Renminbi")
        EUR = "EUR", _("Euro Member Countries")
        RON = "RON", _("Romania Leu")
        GBP = "GBP", _("United Kingdom Pound")
        USD = "USD", _("United States Dollar")

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

    def get_current_period(self, day: date):
        return get_month_range(self.start_day_of_month, day)

    def get_previous_period(self, day: date):
        day_minus_five = day - timedelta(days=5)
        return get_month_range(self.start_day_of_month, day_minus_five)

    def get_next_period(self, day: date):
        day_plus_five = day + timedelta(days=5)
        return get_month_range(self.start_day_of_month, day_plus_five)


class Month(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_("User"), related_name="months", on_delete=models.CASCADE
    )
    first_day = models.DateField()
    last_day = models.DateField(blank=True)
    month_code = models.PositiveSmallIntegerField(blank=True, editable=False)
    override_last_day = models.BooleanField(default=True)

    class Meta:
        unique_together = (("user", "month_code"),)

    def save(self, *args, **kwargs):
        self.month_code = datetime.strftime(self.first_day, "%y%m")
        if self.override_last_day:
            _, self.last_day = get_month_range(self.first_day.day, self.first_day)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_day.strftime('%B')} {self.first_day.year}"


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

    objects = AccountQuerySet.as_manager()

    def get_bg_color(self):
        tailwind_color = "red-500"
        for color in COLOR_PALETTE:
            if color[0] == self.color:
                tailwind_color = color[1]
        return f"bg-{tailwind_color}"

    class Meta:
        ordering = ["-active", "-created_at"]
        unique_together = (("name", "account_type"),)

    def __str__(self):
        return f"{self.name.title()}"

    def save(self, *args, **kwargs):
        self.text_color = "white" if is_color_dark(self.color) else "black"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("wallet:account_detail", kwargs={"pk": self.pk})


class Category(TimeStampedUUIDModel):
    class Group(models.TextChoices):
        INCOME = "IN", _("Income")
        EXPENSE = "EX", _("Expense")
        TRANSFER = "TR", _("Transfer")

    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        related_name="categories",
        on_delete=models.CASCADE,
    )
    group = models.CharField(
        verbose_name=_("Category group"),
        max_length=2,
        choices=Group.choices,
        default=Group.EXPENSE,
    )
    name = models.CharField(_("Name"), max_length=100)
    active = models.BooleanField(verbose_name=_("Active"), default=True)
    color = ColorField(
        verbose_name=_("Color on Dashboard"), samples=COLOR_PALETTE, default="#7DD181"
    )
    text_color = models.CharField(
        verbose_name=_("Text color"), max_length=12, blank=True, editable=False
    )

    objects = CategoryQuerySet.as_manager()

    class Meta:
        verbose_name_plural = _("Categories")
        ordering = ["group", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.text_color = "white" if is_color_dark(self.color) else "black"
        super().save(*args, **kwargs)


class Transaction(TimeStampedUUIDModel):
    class TransactionType(models.TextChoices):
        INCOME = "IN", _("Income")
        EXPENSE = "EX", _("Expense")
        TRANSFER = "TR", _("Transfer")
        ADJUSTMENT = "AD", _("Balance Adjustment")

    class RecurrenceFrequency(models.TextChoices):
        MONTHLY = "MO", _("Monthly")
        QUARTERLY = "QU", _("Quarterly")
        BIANNUALY = "BI", _("Biannualy")
        ANNUALY = "AN", _("Annualy")

    title = models.CharField(verbose_name=_("Title"), max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(default=date.today)
    transaction_type = models.CharField(
        verbose_name=_("Transaction type"),
        max_length=2,
        choices=TransactionType.choices,
    )
    category = models.ForeignKey(
        Category, verbose_name=_("Category"), on_delete=models.PROTECT
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
    is_recurrent = models.BooleanField(verbose_name=_("Is recurrent"), default=False)
    recurrence_frequency = models.CharField(
        verbose_name=_("Recurrence frequency"),
        max_length=2,
        blank=True,
        choices=RecurrenceFrequency.choices,
    )
    is_planned = models.BooleanField(verbose_name=_("Is planned"), default=False)

    objects = TransactionQuerySet.as_manager()

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

    def update_account_balance(self):
        if not self.is_planned:
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_account_balance()

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
        verbose_name=_("Budgeted mount"), max_digits=10, decimal_places=2
    )
    categories = models.ManyToManyField(Category, related_name="budgets")
    month = models.ForeignKey(
        Month, verbose_name=_("Month"), related_name="budgets", on_delete=models.CASCADE
    )
    is_master = models.BooleanField(default=False)

    def __str__(self):
        return self.name
