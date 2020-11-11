from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from tests.transactions.factories import TransactionFactory
from transactions.models import Transaction
from tests.users.factories import UserFactory


class TransactionTestCase(APITestCase):

    def test_create_single_transaction_may_do_it(self):
        user = UserFactory()
        url = reverse('transaction-list')
        request_body = {
            "reference": "000001",
            "account": "S55555",
            "date": "2020-01-01",
            "amount": "21.13",
            "type": "inflow",
            "category": "payment",
            "user_id": user.id
        }

        response = self.client.post(url, request_body)

        expected_response = request_body
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_create_bulk_transactions_may_do_it(self):
        user = UserFactory()
        url = reverse('transaction-list')
        request_body = [
            {
                "reference": "000001",
                "account": "S55555",
                "date": "2020-01-01",
                "amount": "21.13",
                "type": "inflow",
                "category": "transfer",
                "user_id": user.id
            },
            {
                "reference": "000002",
                "account": "S55555",
                "date": "2020-01-01",
                "amount": "-21.13",
                "type": "outflow",
                "category": "payment",
                "user_id": user.id
            }
        ]

        response = self.client.post(url, request_body, format='json')

        expected_response = request_body
        self.assertEquals(status.HTTP_201_CREATED, response.status_code)
        self.assertEquals(expected_response, response.data)

    def test_create_inflow_transaction_with_negative_amount_returns_error(self):
        user = UserFactory()
        url = reverse('transaction-list')
        request_body = {
            "reference": "000001",
            "account": "S55555",
            "date": "2020-01-01",
            "amount": "-21.13",
            "type": "inflow",
            "category": "payment",
            "user_id": user.id
        }

        response = self.client.post(url, request_body)

        expected_response = {'amount': ['Amount must be positive']}
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(expected_response, response.json())

    def test_create_outflow_transaction_with_positive_amount_returns_error(self):
        user = UserFactory()
        url = reverse('transaction-list')
        request_body = {
            "reference": "000001",
            "account": "S55555",
            "date": "2020-01-01",
            "amount": "21.13",
            "type": "outflow",
            "category": "payment",
            "user_id": user.id
        }

        response = self.client.post(url, request_body)

        expected_response = {'amount': ['Amount must be negative']}
        self.assertEquals(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEquals(expected_response, response.json())

    def test_get_balance_of_user_may_do_it_properly(self):
        user = UserFactory()
        TransactionFactory.create_batch(3, user=user)
        url = reverse('transaction-detail', kwargs={'user_id': user.id})

        response = self.client.get(url)

        transaction_number = Transaction.objects.filter(user=user).count()
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(transaction_number, len(response.data['results']))

    def test_get_balance_of_user_filtered_by_before_date_may_do_it_properly(self):
        user = UserFactory()
        date_1 = '2020-01-01'
        date_2 = '2020-10-01'
        TransactionFactory.create_batch(3, user=user, date=date_1)
        TransactionFactory.create_batch(4, user=user, date=date_2)
        url = reverse('transaction-detail', kwargs={'user_id': user.id})
        date_before = '2020-09-01'
        url_with_filter = f'{url}?date_before={date_before}'

        response = self.client.get(url_with_filter)

        transaction_number = Transaction.objects.filter(user=user, date__lt=date_before).count()
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(transaction_number, len(response.data['results']))

    def test_get_balance_of_user_filtered_by_after_date_may_do_it_properly(self):
        user = UserFactory()
        date_1 = '2020-01-01'
        date_2 = '2020-10-01'
        TransactionFactory.create_batch(3, user=user, date=date_1)
        TransactionFactory.create_batch(4, user=user, date=date_2)
        url = reverse('transaction-detail', kwargs={'user_id': user.id})
        date_after = '2020-09-01'
        url_with_filter = f'{url}?date_after={date_after}'

        response = self.client.get(url_with_filter)

        transaction_number = Transaction.objects.filter(user=user, date__gt=date_after).count()
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(transaction_number, len(response.data['results']))

    def test_get_balance_of_user_filtered_by_before_and_after_date_may_do_it_properly(self):
        user = UserFactory()
        date_1 = '2020-01-01'
        date_2 = '2020-05-01'
        date_3 = '2020-10-01'
        TransactionFactory.create_batch(2, user=user, date=date_1)
        TransactionFactory.create_batch(3, user=user, date=date_2)
        TransactionFactory.create_batch(4, user=user, date=date_3)
        url = reverse('transaction-detail', kwargs={'user_id': user.id})
        date_before = '2020-06-01'
        date_after = '2020-04-01'
        url_with_filter = f'{url}?date_before={date_before}&date_after={date_after}'

        response = self.client.get(url_with_filter)

        transaction_number = Transaction.objects.filter(user=user, date__range=[date_after, date_before]).count()
        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertEquals(transaction_number, len(response.data['results']))

    def test_get_user_summary_may_do_it_properly(self):
        user = UserFactory()
        TransactionFactory.create_batch(5, user=user)
        url = reverse('transaction-summary', kwargs={'user_id': user.id})

        response = self.client.get(url)

        self.assertEquals(status.HTTP_200_OK, response.status_code)
        self.assertIsInstance(response.data, dict)
        self.assertIn('inflow', response.data)
        self.assertIsInstance(response.data['inflow'], dict)
        self.assertIn('outflow', response.data)
        self.assertIsInstance(response.data['outflow'], dict)
