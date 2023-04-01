from django.db import models


class AccountQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def shown_on_dashboard(self):
        return self.filter(show_on_dashboard=True)

    def included_from_budget(self):
        return self.filter(exclude_from_budget=False)

    def excluded_from_budget(self):
        return self.filter(exclude_from_budget=True)


class CategoryQuerySet(models.QuerySet):
    def income(self):
        return self.filter(group="IN")

    def expense(self):
        return self.filter(group="EX")

    def transfer(self):
        return self.filter(group="TR")

    def active(self):
        return self.filter(active=True)


class TransactionQuerySet(models.QuerySet):
    def income(self):
        return self.filter(transaction_type="IN")

    def expenses(self):
        return self.filter(transaction_type="EX")

    def transfers(self):
        return self.filter(transaction_type="TR")

    def adjustments(self):
        return self.filter(transaction_type="AD")

    def recurrent(self):
        return self.filter(is_recurring=True)
