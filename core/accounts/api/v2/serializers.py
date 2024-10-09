from rest_framework import serializers 
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from ...models import User, Profile
import re

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

class SigninAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['email', 'is_active']

        read_only_fields = ['is_active']

class ProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name']
        
        read_only_fields = ['is_active', 'email', 'is_staff']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['email'] = instance._user.email 
        representation['is_active'] = instance._user.is_active
        representation['is_staff'] = instance._user.is_staff

        return representation
