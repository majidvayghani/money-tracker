
from rest_framework import serializers 
from accounts.models import User
  
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure that the password is excluded from all response data
    password1 = serializers.CharField(write_only=True)  # Ensure that the password is excluded from all response data

    class Meta: 
        model = User
        fields = ['email','password', 'password1']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)