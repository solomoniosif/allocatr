from datetime import date, datetime, timedelta
from typing import Union

from dateutil.relativedelta import relativedelta
from django.contrib.auth import get_user_model

from .models import Budget, Category, Month, PlannedTransaction, Transaction

User = get_user_model()


def get_or_create_month(
    user: User, date_or_str: Union[datetime.date, str], days_delta: int = 0
) -> Month:
    """Returns existing Month object or generates a new month for the given date
    or month code as string.

    Args:
        user: The user whose month is returned.
        date_or_str: The datetime date or a date in string format to be converted
        to a date.
        days_delta: The number of days before or after the given day

    Returns:
        The month corresponding to the given date or string.
    """
    start_DOM = user.settings.start_day_of_month
    if isinstance(date_or_str, date):
        input_day = date_or_str
    elif isinstance(date_or_str, str):
        date_str = (
            f"{str(start_DOM).rjust(2, '0')}/{date_or_str[-2:]}/{date_or_str[:2]}"
        )
        input_day = datetime.strptime(date_str, "%d/%m/%y").date()
    if days_delta:
        input_day = input_day + relativedelta(days=days_delta)
    if start_DOM <= input_day.day:
        first_day = date(input_day.year, input_day.month, start_DOM)
    else:
        first_day = date(input_day.year, input_day.month, start_DOM) - relativedelta(
            months=1
        )
    current_month, _ = Month.objects.get_or_create(user=user, first_day=first_day)
    return current_month


def get_or_create_next_13_months(user: User) -> list[Month]:
    """Returns a list of the next 12 months for the given user."""
    next_12_months = []
    for i in range(13):
        next_12_months.append(
            get_or_create_month(user, date.today() + relativedelta(months=i))
        )
    return next_12_months


def set_transaction_complete(planned_transaction: PlannedTransaction) -> Transaction:
    """Saves a PlannedTransaction  object as a Transaction object,
    than deletes the PlannedTransaction

    Args:
        planned_transaction: The PlannedTransaction object to be saved as a Transaction.

    Returns:
        The newly created Transaction object.
    """
    new_transaction = Transaction.objects.create(
        title=planned_transaction.title,
        amount=planned_transaction.amount,
        date=planned_transaction.date,
        transaction_type=planned_transaction.transaction_type,
        category=planned_transaction.category,
        account=planned_transaction.account,
        notes=planned_transaction.notes,
    )
    if new_transaction.pkid is not None:
        planned_transaction.delete()
    return new_transaction


def get_budget_stats(budget: Budget) -> dict:
    """A helper function to get the stats for a budget.
    The function collects all transactions and planned transactions
    for the given budget and returns a dictionary with the stats."""
    transactions = Transaction.objects.filter(
        account__user=budget.user,
        category=budget.category,
        date__gte=budget.month.first_day,
        date__lte=budget.month.last_day,
    )
    planned_transactions = PlannedTransaction.objects.filter(
        account__user=budget.user,
        category=budget.category,
        date__gte=budget.month.first_day,
        date__lte=budget.month.last_day,
    )
    subcategories = budget.category.get_all_subcategories()
    for subcategory in subcategories:
        subcategory_transactions = Transaction.objects.filter(
            account__user=budget.user,
            category=subcategory,
            date__gte=budget.month.first_day,
            date__lte=budget.month.last_day,
        )
        transactions = transactions | subcategory_transactions
        subcategory_planned_transactions = PlannedTransaction.objects.filter(
            account__user=budget.user,
            category=subcategory,
            date__gte=budget.month.first_day,
            date__lte=budget.month.last_day,
        )
        planned_transactions = planned_transactions | subcategory_planned_transactions
    amount_completed = sum(t.amount for t in transactions)
    amount_planned = sum(t.amount for t in planned_transactions)
    amount_budgeted = budget.budgeted_amount
    return {
        "category": budget.category.name,
        "categoryId": budget.category.pkid,
        "categoryColor": budget.category.color,
        "completed": float(amount_completed),
        "planned": float(amount_planned),
        "budgeted": float(amount_budgeted),
        "remaining": float(amount_budgeted - amount_completed - amount_planned),
        "categoryTotal": float(max(amount_budgeted, amount_completed + amount_planned)),
    }


def get_or_create_master_budget(month: Month) -> Budget:
    """Returns the master budget for the given month.
    If the master budget does not exist, it creates it."""
    master_budget, _ = Budget.objects.get_or_create(
        user=month.user, is_master=True, month=month
    )
    return master_budget


def get_category_stats(category: Category, month: Month) -> dict:
    """A helper function to get the stats for a category."""
    transactions = Transaction.objects.filter(
        account__user=category.user,
        category=category,
        date__gte=month.first_day,
        date__lte=month.last_day,
    )
    planned_transactions = PlannedTransaction.objects.filter(
        account__user=category.user,
        category=category,
        date__gte=month.first_day,
        date__lte=month.last_day,
    )
    subcategories = category.get_all_subcategories()
    for subcategory in subcategories:
        subcategory_transactions = Transaction.objects.filter(
            account__user=category.user,
            category=subcategory,
            date__gte=month.first_day,
            date__lte=month.last_day,
        )
        transactions = transactions | subcategory_transactions
        subcategory_planned_transactions = PlannedTransaction.objects.filter(
            account__user=category.user,
            category=subcategory,
            date__gte=month.first_day,
            date__lte=month.last_day,
        )
        planned_transactions = planned_transactions | subcategory_planned_transactions
    amount_completed = sum(t.amount for t in transactions)
    amount_planned = sum(t.amount for t in planned_transactions)
    return {
        "category": category.name,
        "categoryId": category.pkid,
        "categoryColor": category.color,
        "completed": float(amount_completed),
        "planned": float(amount_planned),
        "budgeted": 0,
        "categoryTotal": float(amount_completed + amount_planned),
    }


def get_master_budget_stats(month: Month) -> dict:
    """Returns the stats for the master budget for the given month."""
    master_budget, _ = Budget.objects.get_or_create(
        user=month.user, month=month, is_master=True
    )
    expense_categories = []
    root_expense_categories = Category.objects.filter(
        user=month.user, group="EX", parent=None
    )
    for category in root_expense_categories:
        try:
            budget = Budget.objects.get(user=month.user, month=month, category=category)
            expense_categories.append(get_budget_stats(budget))
        except Budget.DoesNotExist:
            expense_categories.append(get_category_stats(category, month))
    income_categories = []
    root_income_categories = Category.objects.filter(
        user=month.user, group="IN", parent=None
    )
    for category in root_income_categories:
        try:
            budget = Budget.objects.get(user=month.user, month=month, category=category)
            income_categories.append(get_budget_stats(budget))
        except Budget.DoesNotExist:
            income_categories.append(get_category_stats(category, month))
    total_spent = sum(c["completed"] for c in expense_categories)
    total_income = sum(c["completed"] for c in income_categories)
    total_budget_expense = sum(c["categoryTotal"] for c in expense_categories)
    total_budget_income = sum(c["categoryTotal"] for c in income_categories)
    unallocated = float(master_budget.budgeted_amount) - total_budget_expense
    return {
        "budgetedAmount": float(master_budget.budgeted_amount),
        "totalSpent": total_spent,
        "totalIncome": total_income,
        "totalBudgetExpense": total_budget_expense,
        "totalBudgetIncome": total_budget_income,
        "expenseCategories": expense_categories,
        "incomeCategories": income_categories,
        "unallocatedAmount": unallocated,
        "monthName": month.__str__(),
    }


def get_current_month_expenses(user: User) -> dict:
    """Returns the current month's expenses."""
    month = get_or_create_month(user, date.today())
    month_days = [month.first_day + timedelta(days=i) for i in range(month.month_days)]
    all_month_expenses = Transaction.objects.filter(
        account__user=user,
        date__gte=month.first_day,
        date__lte=month.last_day,
        transaction_type="EX",
    )
    actual_expenses = [0 for _ in range(month.month_days)]
    for index, day in enumerate(month_days):
        if day <= date.today():
            day_expenses = all_month_expenses.filter(date=day)
            day_expense_amount = int(sum(t.amount for t in day_expenses)) or 0
            if index == 0:
                actual_expenses[index] = day_expense_amount
            else:
                actual_expenses[index] = actual_expenses[index - 1] + day_expense_amount
    rest_of_month_planned_expenses = PlannedTransaction.objects.filter(
        account__user=user,
        date__gte=date.today(),
        date__lte=month.last_day,
        transaction_type="EX",
    )
    planned_expenses = [0 for _ in range(month.month_days)]
    for index, day in enumerate(month_days):
        if day == date.today():
            planned_expenses[index] = actual_expenses[index]
        if day >= date.today():
            day_expenses = rest_of_month_planned_expenses.filter(date=day)
            day_expense_amount = int(sum(t.amount for t in day_expenses)) or 0
            if index == 0:
                planned_expenses[index] = day_expense_amount
            else:
                planned_expenses[index] = (
                    planned_expenses[index - 1] + day_expense_amount
                )
    month_days_str = [day.strftime("%d-%m") for day in month_days]
    return {
        "monthDays": month_days_str,
        "actualExpenses": [None if i == 0 else i for i in actual_expenses],
        "plannedExpenses": [None if i == 0 else i for i in planned_expenses],
    }
