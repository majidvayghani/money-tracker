# transactions/serializers.py
from rest_framework import serializers
from ...models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['_id', '_profile', 'amount', 'category', 'description', 'tag']
        read_only_fields = ['_id', '_profile']

    def create(self, validated_data):
        """
        Overriding the create method to assign the profile from the request context.
        """
        _profile = self.context['request'].user.profile
        return Transaction.objects.create(_profile=_profile, **validated_data)

    def update(self, instance, validated_data):
        """
        Overriding the update method for partial update of transaction.
        """
        instance.amount = validated_data.get('amount', instance.amount)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.save()
        return instance
