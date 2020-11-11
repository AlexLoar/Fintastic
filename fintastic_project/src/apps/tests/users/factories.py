import random

from django.contrib.auth import get_user_model

import factory
from faker import Factory

faker = Factory.create()


class UserFactory(factory.django.DjangoModelFactory):
    name = factory.lazy_attribute(lambda o: faker.name())
    email = factory.lazy_attribute(lambda o: f'{o.name}@example.com')
    age = factory.lazy_attribute(lambda o: random.randint(1, 90))

    class Meta:
        model = get_user_model()
