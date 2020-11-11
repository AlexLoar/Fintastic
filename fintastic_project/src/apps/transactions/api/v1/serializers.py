from rest_framework import serializers

from transactions.models import Transaction
from transactions.services import TransactionService


class TransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = ['reference', 'account', 'date', 'amount', 'type', 'category', 'user_id']

    def validate(self, data):
        transaction_type = data['type']
        amount = data['amount']
        is_valid, message = TransactionService.validate_amount(transaction_type=transaction_type,
                                                               amount=amount)
        if not is_valid:
            raise serializers.ValidationError({'amount': message})

        return data


class TransactionOutputSerializer(serializers.ModelSerializer):
    account = serializers.CharField()
    balance = serializers.DecimalField(max_digits=8, decimal_places=2)
    total_inflow = serializers.DecimalField(max_digits=8, decimal_places=2)
    total_outflow = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        model = Transaction
        fields = ['account', 'balance', 'total_inflow', 'total_outflow']
