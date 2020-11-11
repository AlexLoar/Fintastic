from django.db.models import Sum, F, Q, QuerySet
from django.db.models.functions import Coalesce

from transactions.models import Transaction


class TransactionService:

    @classmethod
    def validate_amount(cls, transaction_type: str, amount: float) -> (bool, str):
        is_valid = True
        message = ''
        if transaction_type == Transaction.OUTFLOW:
            if amount >= 0:
                is_valid = False
                message = 'Amount must be negative'
        elif transaction_type == Transaction.INFLOW:
            if amount <= 0:
                is_valid = False
                message = 'Amount must be positive'

        return is_valid, message

    @classmethod
    def calculate_balance(cls, transactions: QuerySet) -> QuerySet:
        return transactions.values('account')\
            .annotate(total_inflow=Coalesce(Sum('amount', filter=Q(type=Transaction.INFLOW)), 0),
                      total_outflow=Coalesce(Sum('amount', filter=Q(type=Transaction.OUTFLOW)), 0)
                      )\
            .annotate(balance=F('total_inflow') + F('total_outflow'))

    @classmethod
    def calculate_summary(cls, user_id: str) -> dict:
        transactions = Transaction.objects.filter(user_id=user_id)
        inflow_result = cls.__get_partial_summary(transactions, Transaction.INFLOW)
        outflow_result = cls.__get_partial_summary(transactions, Transaction.OUTFLOW)

        return {
            'inflow': inflow_result,
            'outflow': outflow_result
        }

    @classmethod
    def __get_partial_summary(cls, transactions: QuerySet, transaction_type: str) -> dict:
        partial_result = {}
        partial_transactions = transactions.filter(type=transaction_type).values('category').annotate(inflow=Sum('amount'))
        for partial_transaction in partial_transactions:
            partial_result.update(dict([tuple(partial_transaction.values())]))
        return partial_result
