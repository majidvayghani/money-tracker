
from rest_framework import serializers 
from accounts.models import CustomUser 
  
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure that the password is excluded from all response data
    
    class Meta: 
        model = CustomUser 
        fields = ['id', 'email','password', 'is_active', 'is_staff']

        read_only_fields = ('is_active', 'is_staff')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)