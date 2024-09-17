
from rest_framework import serializers 
from accounts.models import User

  
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure that the password is excluded from all response data
    password1 = serializers.CharField(write_only=True)  # Ensure that the password is excluded from all response data

    class Meta: 
        model = User
        fields = ['email','password', 'password1']

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({'error' : 'passwordd dosent match!'})
        
        return super().validate(attrs)
    
    def create(self, validated_data):
        validated_data.pop('password1')
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)