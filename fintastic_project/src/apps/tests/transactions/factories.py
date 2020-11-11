import random

import factory
from faker import Factory

from transactions.models import Transaction
from tests.users.factories import UserFactory

faker = Factory.create()


TYPE_CHOICES = [Transaction.INFLOW, Transaction.OUTFLOW]
CATEGORY_CHOICES = ['groceries', 'salary', 'transfer', 'rent', 'savings']


def generate_amount(type_: str) -> float:
    random_float = round(random.uniform(1, 90), 2)
    return random_float if type_ == Transaction.OUTFLOW else random_float * -1


class TransactionFactory(factory.django.DjangoModelFactory):

    reference = factory.lazy_attribute(lambda o: faker.ean(length=8))
    account = factory.lazy_attribute(lambda o: faker.iban())
    date = factory.lazy_attribute(lambda o: faker.date())
    type = factory.lazy_attribute(lambda o: random.choice(TYPE_CHOICES))
    amount = factory.lazy_attribute(lambda o: generate_amount(o.type))
    category = factory.lazy_attribute(lambda o: random.choice(CATEGORY_CHOICES))
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Transaction
