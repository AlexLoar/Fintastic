from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from transactions.models import Transaction
from transactions.services import TransactionService
from transactions.api.v1.filterset import TransactionFilter
from transactions.api.v1.serializers import TransactionSerializer, TransactionOutputSerializer


class TransactionView(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    lookup_field = 'user_id'
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TransactionFilter

    def create(self, request, *args, **kwargs):
        serializer = self._get_transaction_serializer()

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _get_transaction_serializer(self, *args, **kwargs):
        is_bulk = isinstance(self.request.data, list)
        if is_bulk:
            serializer = self.serializer_class(data=self.request.data, many=True)
        else:
            serializer = self.serializer_class(data=self.request.data)
        return serializer

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs['user_id']

        transactions = Transaction.objects.filter(user_id=user_id)
        filtered_transactions = self.filter_queryset(transactions)
        processed_transactions = TransactionService.calculate_balance(filtered_transactions)
        paginated_transactions = self.paginate_queryset(processed_transactions)
        serializer = TransactionOutputSerializer(paginated_transactions, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=['GET'], detail=True, url_path='summary', url_name='summary')
    def summary(self, request, user_id: str):
        processed_transactions = TransactionService.calculate_summary(user_id)
        return Response(processed_transactions)
