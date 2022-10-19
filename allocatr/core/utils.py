from django.core.exceptions import ValidationError

from .models import Transaction


def update_transaction(old_t: Transaction, new_t: Transaction) -> None:
    if old_t.transaction_type != new_t.transaction_type:
        raise ValidationError(
            "Cannot change transaction type. Delete the first transaction than add a new one."
        )

    t_type = old_t.transaction_type
    if t_type == Transaction.TransactionType.INCOME:
        if old_t.account == new_t.account and old_t.amount == new_t.amount:
            pass
        else:
            old_a = old_t.account
            new_a = new_t.account
            old_a.balance -= old_t.amount
            old_a.save()
            new_a.balance += new_t.amount
            new_a.save()

    elif t_type == Transaction.TransactionType.EXPENSE:
        if old_t.account == new_t.account and old_t.amount == new_t.amount:
            pass
        else:
            old_a = old_t.account
            new_a = new_t.account
            old_a.balance += old_t.amount
            old_a.save()
            new_a.balance -= new_t.amount
            new_a.save()

    elif t_type == Transaction.TransactionType.TRANSFER:
        if (
            old_t.account == new_t.account
            and old_t.amount == new_t.amount
            and old_t.dest_account == new_t.dest_account
        ):
            pass
        else:
            old_a = old_t.account
            new_a = new_t.account
            old_dest_a = old_t.dest_account
            new_dest_a = new_t.dest_account
            old_a.balance += old_t.amount
            old_a.save()
            new_a.balance -= new_t.amount
            new_a.save()
            old_dest_a.balance -= old_t.amount
            new_dest_a.balance += new_t.amount
