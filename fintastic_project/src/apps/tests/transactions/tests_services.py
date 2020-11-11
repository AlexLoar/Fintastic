from decimal import Decimal
from unittest import TestCase

from transactions.services import TransactionService, Transaction
from tests.transactions.factories import TransactionFactory
from tests.users.factories import UserFactory


class TransactionServiceTestCase(TestCase):
    def test_validate_amount_when_outflow_is_positive_returns_false(self):
        outflow_transaction = Transaction.OUTFLOW
        amount = 10
        is_valid, message = TransactionService.validate_amount(transaction_type=outflow_transaction,
                                                               amount=amount)

        expected_message = 'Amount must be negative'
        self.assertFalse(is_valid)
        self.assertEquals(expected_message, message)

    def test_validate_amount_when_outflow_is_negative_returns_true(self):
        outflow_transaction = Transaction.OUTFLOW
        amount = -10
        is_valid, message = TransactionService.validate_amount(transaction_type=outflow_transaction,
                                                               amount=amount)

        expected_message = ''
        self.assertTrue(is_valid)
        self.assertEquals(expected_message, message)

    def test_validate_amount_when_inflow_is_negative_returns_false(self):
        inflow_transaction = Transaction.INFLOW
        amount = -10
        is_valid, message = TransactionService.validate_amount(transaction_type=inflow_transaction,
                                                               amount=amount)

        expected_message = 'Amount must be positive'
        self.assertFalse(is_valid)
        self.assertEquals(expected_message, message)

    def test_validate_amount_when_inflow_is_positive_returns_true(self):
        inflow_transaction = Transaction.INFLOW
        amount = 10
        is_valid, message = TransactionService.validate_amount(transaction_type=inflow_transaction,
                                                               amount=amount)

        expected_message = ''
        self.assertTrue(is_valid)
        self.assertEquals(expected_message, message)

    def test_calculate_balance_may_do_it_properly(self):
        user = UserFactory()
        account_1 = '00001'
        inflow_transaction_1_account_1 = TransactionFactory(type=Transaction.INFLOW, account=account_1, user=user)
        inflow_transaction_2_account_1 = TransactionFactory(type=Transaction.INFLOW, account=account_1, user=user)
        outflow_transaction_1_account_1 = TransactionFactory(type=Transaction.OUTFLOW, account=account_1, user=user)
        outflow_transaction_2_account_1 = TransactionFactory(type=Transaction.OUTFLOW, account=account_1, user=user)

        total_inflow_account_1 = round(Decimal(inflow_transaction_1_account_1.amount + inflow_transaction_2_account_1.amount), 2)
        total_outflow_account_1 = round(Decimal(outflow_transaction_1_account_1.amount + outflow_transaction_2_account_1.amount), 2)
        balance_account_1 = round(Decimal(total_inflow_account_1 + total_outflow_account_1), 2)

        account_2 = '00002'
        inflow_transaction_1_account_2 = TransactionFactory(type=Transaction.INFLOW, account=account_2, user=user)
        inflow_transaction_2_account_2 = TransactionFactory(type=Transaction.INFLOW, account=account_2, user=user)
        outflow_transaction_1_account_2 = TransactionFactory(type=Transaction.OUTFLOW, account=account_2, user=user)
        outflow_transaction_2_account_2 = TransactionFactory(type=Transaction.OUTFLOW, account=account_2, user=user)

        total_inflow_account_2 = round(Decimal(inflow_transaction_1_account_2.amount + inflow_transaction_2_account_2.amount), 2)
        total_outflow_account_2 = round(Decimal(outflow_transaction_1_account_2.amount + outflow_transaction_2_account_2.amount), 2)
        balance_account_2 = round(Decimal(total_inflow_account_2 + total_outflow_account_2), 2)

        transactions = Transaction.objects.filter(user=user)
        queryset = TransactionService.calculate_balance(transactions)

        expected_account_1 = {'account': '00001',
                              'total_inflow': total_inflow_account_1,
                              'total_outflow': total_outflow_account_1,
                              'balance': balance_account_1
                              }
        expected_account_2 = {'account': '00002',
                              'total_inflow': total_inflow_account_2,
                              'total_outflow': total_outflow_account_2,
                              'balance': balance_account_2
                              }
        self.assertEquals(expected_account_1, queryset[0])
        self.assertEquals(expected_account_2, queryset[1])

    def test_calculate_summary_may_do_it_properly(self):
        user = UserFactory()
        TransactionFactory.create_batch(5, user=user)

        summary = TransactionService.calculate_summary(user.id)

        self.assertIsInstance(summary, dict)
        self.assertIn('inflow', summary)
        self.assertIsInstance(summary['inflow'], dict)
        self.assertIn('outflow', summary)
        self.assertIsInstance(summary['outflow'], dict)
