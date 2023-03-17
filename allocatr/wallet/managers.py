from django.db import models


class IncomeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group="IN")


class ExpenseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group="EX")


class TransferManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(group="TR")
