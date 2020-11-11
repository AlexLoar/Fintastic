from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import filters

from transactions.models import Transaction


class TransactionFilter(FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Transaction
        fields = ['date']
