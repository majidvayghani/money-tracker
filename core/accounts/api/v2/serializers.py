from rest_framework import serializers 
from django.contrib.auth import get_user_model
from tokens.models import Token
import re

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_password(self, value):
        # Password length validation
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        
        # Must include at least one digit
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        
        # Must include at least one uppercase letter
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must contain at least one uppercase letter.")
        
        # Must include at least one lowercase letter
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Password must contain at least one lowercase letter.")
        
        # Must include at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")

        return value

    # create_user is a method provided by the User model's manager (objects) in Django's authentication system
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email", write_only=True)
    password = serializers.CharField(label="Password", write_only=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Step 1: Check if the user exists
        user = User.get_user_by_email(email)
        if not user:
            raise serializers.ValidationError("User not found!")

        # Step 2: Check if the user is active
        if not user.is_active:
            raise serializers.ValidationError("User is deleted or inactive!")

        # Step 3: Check if the password is correct
        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password!")

        # If all checks pass, add the user to attrs
        attrs['user'] = user
        return attrs

class SignoutSerializer(serializers.Serializer):
    def validate(self, attrs):
        request = self.context['request']
        token_obj = request.auth
        user = request.user

        if not isinstance(token_obj, Token):
            raise serializers.ValidationError("Invalid or missing token.")

        if token_obj._user != user or not token_obj.is_active:
            raise serializers.ValidationError("Invalid or expired token.")

        self.token_obj = token_obj
        return attrs

    def save(self, **kwargs):
        self.token_obj.is_active = False
        self.token_obj.save()
        return self.token_obj

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['email', 'is_active']

        read_only_fields = ['is_active']