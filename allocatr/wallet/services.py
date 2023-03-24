from datetime import date, datetime
from typing import Union
from dateutil.relativedelta import relativedelta

from django.contrib.auth import get_user_model

from .models import Month

User = get_user_model()


def get_or_create_month(
    user: User, date_or_str: Union[datetime.date, str], days_delta: int = 0
) -> Month:
    """Returns existing Month object or generates a new month for the given date
    or month code as string.

    Args:
        user: The user whose month is returned.
        date_or_str: The date or string to be converted to a date.
        days_delta: The number of days before or after the given day

    Returns:
        The month corresponding to the given date or string.
    """
    start_day_of_month = user.settings.start_day_of_month
    if isinstance(date_or_str, date):
        input_day = date_or_str
    elif isinstance(date_or_str, str):
        date_str = (
            f"{str(start_day_of_month).rjust(2, '0')}/{date_or_str[-2:]}/{date_or_str[:2]}"
        )
        input_day = datetime.strptime(date_str, "%d/%m/%y").date()
    if days_delta:
        input_day = input_day + relativedelta(days=days_delta)
    if start_day_of_month <= input_day.day:
        first_day = date(input_day.year, input_day.month, start_day_of_month)
    else:
        first_day = date(
            input_day.year, input_day.month, start_day_of_month
        ) - relativedelta(months=1)
    current_month, _ = Month.objects.get_or_create(user=user, first_day=first_day)
    return current_month