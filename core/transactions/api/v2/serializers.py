from rest_framework import serializers 
from transactions.models import Transaction 
  
class TransactionSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = Transaction 
        fields = ['amount','description', 'category', 'created_at', 'updated_at']

        read_only_fields = ['created_at', 'updated_at']

    def validate_amount(self, value):
        """validation methods"""
        if value <= 0:
          raise serializers.ValidationError("Amount must be greater than zero.")
        return value
    
    def create(self, validated_data):
        """
        Create a Transaction instance, associating it with the authenticated user.
        """
        user = self.context.get('user')
        if not user:
            raise serializers.ValidationError("User must be provided in the context.")
        return Transaction.objects.create(_user=user, **validated_data)