
from rest_framework import serializers 
from transactions.models import Transaction 
  
class TransactionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Transaction 
        fields = "__all__"

        read_only_fields = ('created_at', 'updated_at')

        def validate_amount(self, value):
            """validation methods"""
            if value <= 0:
              raise serializers.ValidationError("Amount must be greater than zero.")
            return value
