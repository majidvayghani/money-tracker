from rest_framework import serializers 
from transactions.models import Transaction, TransactionCategory
  
class TransactionSerializer(serializers.ModelSerializer):
    origin  = serializers.SerializerMethodField()

    class Meta: 
        model = Transaction 
        fields = ['amount','description', '_category', 'created_at', 'soft_deleted_at', '_user', 'origin']

        read_only_fields = ['_user', 'created_at', 'soft_deleted_at', 'origin']

    def get_origin(self, obj):
        # Access context to modify extra_field dynamically
        return self.context.get('origin', 'db')
         

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
    
class TransactionCreateSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Transaction 
        fields = ['amount','description', '_category', 'created_at', 'soft_deleted_at', '_user']

        read_only_fields = ['_user', 'created_at', 'soft_deleted_at']


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
    
class TransactionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCategory
        fields = ['_id', 'name', 'parent', 'is_income', 'is_expense']