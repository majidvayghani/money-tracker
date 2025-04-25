from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from tokens.models import Token

class CustomTokenAuthentication(BaseAuthentication):
    keyword = 'Token'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None

        try:
            keyword, token_key = auth_header.split()
        except ValueError:
            raise AuthenticationFailed('Invalid token header.')

        if keyword != self.keyword:
            return None

        try:
            token = Token.objects.get(token=token_key, is_active=True)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid or expired token.')

        if token.is_expired():
            token.is_active = False
            token.save()
            raise AuthenticationFailed('Token has expired.')

        return (token._user, token)
