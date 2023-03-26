from django.db import models

# Create a custom manager
# that can be used both with Transaction and PlannedTransaction models


class TransactionManager(models.Manager):
    def for_month(self, month):
        return self.filter(date__gte=month.first_day, date__lte=month.last_day)
