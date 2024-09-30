from rest_framework import serializers 
from accounts.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']
    
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

class UserProfileSerializer(serializers.ModelSerializer):    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'is_active', 'updated_at']

        read_only_fields = ['is_active', 'updated_at']
