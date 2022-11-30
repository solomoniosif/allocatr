from django.db.models.signals import post_save
from django.dispatch import receiver

from .models.transaction import Transaction
from .utils import update_transaction


@receiver(post_save, sender=Transaction)
def update_account_balance(sender, instance, created, **kwargs):
    if instance.pkid is not None:
        current_transaction = instance
        previous_transaction = Transaction.objects.get(pkid=instance.pkid)
        update_transaction(previous_transaction, current_transaction)
    else:
        account = instance.account
        if instance.type == instance.TransactionType.INCOME:
            account.balance += instance.amount
            account.save()
        elif instance.type == instance.TransactionType.EXPENSE:
            account.balance -= instance.amount
            account.save()
        elif instance.type == instance.TransactionType.TRANSFER:
            account.balance -= instance.amount
            account.save()
            dest_account = instance.dest_account
            dest_account.balance += instance.amount
            dest_account.save()


# @receiver(post_save, sender=Transaction, dispatch_uid="income_pre_save")
# def update_account_balance_on_transaction_create(sender, instance, created, **kwargs):
#     if created:
#         print("»» post_save Signal run")
#         account = instance.account
#         if instance.type == instance.TransactionType.INCOME:
#             account.balance += instance.amount
#             account.save()
#         elif instance.type == instance.TransactionType.EXPENSE:
#             account.balance -= instance.amount
#             account.save()
#         elif instance.type == instance.TransactionType.TRANSFER:
#             account.balance -= instance.amount
#             account.save()
#             dest_account = instance.dest_account
#             dest_account.balance += instance.amount
#             dest_account.save()


# @receiver(post_delete, sender=Income)
# def update_account_balance_on_transaction_delete(sender, instance, **kwargs):
#     t_type = instance.type
#     if t_type == instance.TransactionType.INCOME:
#         account = instance.account
#         account.balance -= instance.amount
#         account.save()
#     elif t_type == instance.TransactionType.EXPENSE:
#         account = instance.account
#         account.balance += instance.amount
#         account.save()
#     elif t_type == instance.TransactionType.TRANSFER:
#         account = instance.account
#         dest_account = instance.dest_account
#         account.balance += instance.amount
#         account.save()
#         dest_account.balance -= instance.amount
#         dest_account.save()
