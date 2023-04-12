import uuid
from datetime import date, datetime

from colorfield.fields import ColorField
from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
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


class Month(models.Model):
    user = models.ForeignKey(
        User, verbose_name=_("User"), related_name="months", on_delete=models.CASCADE
    )
    first_day = models.DateField()
    last_day = models.DateField(blank=True)
    month_code = models.PositiveSmallIntegerField(
        blank=True,
        editable=False,
        validators=[
            RegexValidator(
                regex=r"^\d{4}$", message="Month code must be 4 digits long"
            ),
            RegexValidator(
                regex=r"^\d{2}$",
                message="Last 2 digits of month code must be between 01 and 12",
                code="invalid_month_code",
            ),
            RegexValidator(
                regex=r"^(0[1-9]|1[0-2])$",
                message="Last 2 digits of month code must be between 01 and 12",
                code="invalid_month_code",
            ),
        ],
    )
    override_last_day = models.BooleanField(default=True)
    month_days = models.PositiveSmallIntegerField(default=0, editable=False)

    def get_or_create_next_month(self):
        next_month = (
            Month.objects.filter(user=self.user, first_day__gt=self.first_day)
            .order_by("first_day")
            .first()
        )
        if not next_month:
            next_month = Month.objects.create(
                user=self.user, first_day=self.first_day + relativedelta(months=1)
            )
        return next_month

    def get_or_create_previous_month(self):
        previous_month = (
            Month.objects.filter(user=self.user, first_day__lt=self.first_day)
            .order_by("-first_day")
            .first()
        )
        if not previous_month:
            previous_month = Month.objects.create(
                user=self.user, first_day=self.first_day - relativedelta(months=1)
            )
        return previous_month

    class Meta:
        unique_together = (("user", "month_code"),)
        ordering = ("-first_day",)

    def save(self, *args, **kwargs):
        self.month_code = datetime.strftime(self.first_day, "%y%m")
        if self.override_last_day:
            _, self.last_day = get_month_range(self.first_day.day, self.first_day)
        self.month_days = (self.last_day - self.first_day).days + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_day.strftime('%B')} {self.first_day.year}"


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
    show_decimal_places = models.BooleanField(default=True)
    start_day_of_month = models.PositiveSmallIntegerField(
        default=1,
        validators=[
            MaxValueValidator(28, message=_("Value must be between 1 and 28.")),
            MinValueValidator(1, message=_("Value must be between 1 and 28.")),
        ],
    )

    class Meta:
        verbose_name_plural = "User Settings"

    def save(self, *args, **kwargs):
        # Check if object is being updated and if start_day_of_month has changed
        if (
            not self._state.adding
            and self.start_day_of_month
            != self.__class__.objects.get(pk=self.pk).start_day_of_month
        ):
            # If start_day_of_month has changed, update all months
            self.update_all_following_months(self.start_day_of_month)
        super().save(*args, **kwargs)

    def update_all_following_months(self, new_start_day_of_month: int):
        # Get all following months and update them
        following_months = Month.objects.filter(
            first_day__gte=date.today(), user=self.user
        )
        for month in following_months:
            month.first_day = month.first_day.replace(day=new_start_day_of_month)
            month.save()


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
        return str(self.name)

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
    parent = models.ForeignKey(
        "self",
        related_name="subcategories",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    root_category = models.ForeignKey(
        "self",
        related_name="all_subcategories",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
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
        ordering = ["group", "parent__id", "id"]

    def get_all_subcategories(self):
        """Returns a queryset of all descendent categories (subcategories)"""
        descendents = []
        subcategories = self.subcategories.all()
        for subcategory in subcategories:
            descendents.append(subcategory)
            descendents.extend(subcategory.get_all_subcategories())
        return descendents

    def __str__(self):
        return str(self.name) if not self.parent else f"⤷ {self.name}"

    def save(self, *args, **kwargs):
        self.text_color = "white" if is_color_dark(self.color) else "black"
        if (
            self._state.adding
            or self.parent != self.__class__.objects.get(pkid=self.pkid).parent
        ):
            if self.parent:
                self.root_category = self.parent.root_category
            else:
                super().save(*args, **kwargs)
                self.root_category = self
                self.save()
            for child in self.subcategories.all():
                child.save()
        super().save(*args, **kwargs)


class Transaction(TimeStampedUUIDModel):
    class TransactionType(models.TextChoices):
        INCOME = "IN", _("Income")
        EXPENSE = "EX", _("Expense")
        TRANSFER = "TR", _("Transfer")
        ADJUSTMENT = "AD", _("Balance Adjustment")

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

    objects = TransactionQuerySet.as_manager()

    class Meta:
        ordering = ["-date"]

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
        self.update_account_balance()
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
        return hash(self.id)

    def __eq__(self, other):
        return self.pkid == other.pkid

    def is_income(self):
        return self.transaction_type == self.TransactionType.INCOME

    def is_expense(self):
        return self.transaction_type == self.TransactionType.EXPENSE

    def is_transfer(self):
        return self.transaction_type == self.TransactionType.TRANSFER


class PlannedTransaction(TimeStampedUUIDModel):
    class TransactionType(models.TextChoices):
        INCOME = "IN", _("Income")
        EXPENSE = "EX", _("Expense")

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
        Category,
        verbose_name=_("Category"),
        related_name="planned_transactions",
        on_delete=models.PROTECT,
    )
    account = models.ForeignKey(
        Account,
        verbose_name=_("Account"),
        related_name="planned_transactions",
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
    is_recurring = models.BooleanField(default=False)
    recurrence_frequency = models.CharField(
        max_length=2, choices=RecurrenceFrequency.choices, blank=True, null=True
    )
    recurrence_id = models.UUIDField(blank=True, null=True)
    is_duplicated = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def duplicate_recurring_transaction(self):
        if self.recurrence_frequency == self.RecurrenceFrequency.MONTHLY:
            next_date = self.date + relativedelta(months=1)
            if next_date > date.today() + relativedelta(months=1, days=15):
                return False
        elif self.recurrence_frequency == self.RecurrenceFrequency.QUARTERLY:
            next_date = self.date + relativedelta(months=3)
            if next_date > date.today() + relativedelta(months=3, days=15):
                return False
        elif self.recurrence_frequency == self.RecurrenceFrequency.BIANNUALY:
            next_date = self.date + relativedelta(months=6)
            if next_date > date.today() + relativedelta(months=6, days=15):
                return False
        elif self.recurrence_frequency == self.RecurrenceFrequency.ANNUALY:
            next_date = self.date + relativedelta(years=1)
            if next_date > date.today() + relativedelta(years=1, days=15):
                return False

        delimiter = self.title.rfind("|")
        if delimiter != -1:
            new_title = self.title[:delimiter] + f" | {next_date.strftime('%B %Y')}"
        else:
            new_title = f"{self.title} | {next_date.strftime('%B %Y')}"

        new_transaction = PlannedTransaction(
            title=new_title,
            amount=self.amount,
            date=next_date,
            transaction_type=self.transaction_type,
            category=self.category,
            account=self.account,
            to_account=self.to_account,
            notes=self.notes,
            is_recurring=self.is_recurring,
            recurrence_frequency=self.recurrence_frequency,
            recurrence_id=self.recurrence_id or self.id,
            is_duplicated=False,
            is_completed=False,
        )
        new_transaction.save()
        return True

    def save(self, *args, **kwargs):
        if not self.recurrence_id:
            self.recurrence_id = self.id
        if self.is_recurring and not self.is_duplicated:
            was_duplicated = self.duplicate_recurring_transaction()
            self.is_duplicated = was_duplicated
        super().save(*args, **kwargs)


class Budget(TimeStampedUUIDModel):
    user = models.ForeignKey(
        User, verbose_name=_("User"), related_name="budgets", on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_("Name"), max_length=150, blank=True, null=True
    )
    budgeted_amount = models.DecimalField(
        verbose_name=_("Budgeted mount"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        related_name="budgets",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    month = models.ForeignKey(
        Month, verbose_name=_("Month"), related_name="budgets", on_delete=models.CASCADE
    )
    is_master = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "category", "month")

    def __str__(self):
        return self.name

    def clean(self):
        if self.category and self.is_master:
            raise ValidationError(
                "You cannot select both a category and set is_master to True."
            )

    def save(self, *args, **kwargs):
        if not self.name:
            if self.category:
                self.name = f"{self.category.name} budget for {self.month}"
            else:
                self.name = f"Master budget for {self.month}"
        super().save(*args, **kwargs)
