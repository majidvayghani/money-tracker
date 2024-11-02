
import time
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token

class RateLimitMiddleware(MiddlewareMixin):
    """
        Key Factors:
        Prefix: Ratelimit
        Key Pattern: Ratelimit:u:<User_id>
        u<User_id> represents the user ID
        Return Format: "Ratelimit:u:<uid>"
    """

    """
        Public routes: /api/v2/signin, /api/v2/signup, /admin
        Steps:
            1- Any API call to public routes has a rate limit of RATE_LIMIT_PUBLIC
            2- Any authenticated API call has a rate limit of RATE_LIMIT_AUTHENTICATED
            3- If an API call is not authenticated, it will have a rate limit of RATE_LIMIT_PUBLIC
        Rate Limits:
        Rate limit for step 2: 10 API calls per 1 minute
        Rate limit for other steps: 5 API calls per 1 minute
    """

    PUBLIC_ROUTES = ['/api/v2/signin', '/api/v2/signup', '/admin']
    RATE_LIMIT_PUBLIC = 5  # 5 requests per minute for unauthenticated users and public endpoints
    RATE_LIMIT_AUTHENTICATED = 10  # 10 requests per minute for authenticated users
    RATE_LIMIT_DURATION = 60  # in seconds

    def authenticate_user(self, request):
        """
            Retrieve token from headers because:
            In Django, middlewares execute before view-level authentication (such as DRF’s token authentication),
            so request.user might not be populated yet
        """
        auth_header = get_authorization_header(request).decode('utf-8')
        if auth_header.startswith('Token '):
            token_key = auth_header.split(' ')[1]
            try:
                token = Token.objects.get(key=token_key)
                # Return user ID and authenticated status
                return token.user._id, True
            except Token.DoesNotExist:
                # Token not found, return None
                return None, False
        # No token provided, unauthenticated user
        return None, False

    def process_request(self, request):
        path = request.path
        token = get_authorization_header(request).split()
        user_id, authenticated = self.authenticate_user(request)

        if path in self.PUBLIC_ROUTES:
            rate_limit = self.RATE_LIMIT_PUBLIC 

        else:
            if authenticated:
                rate_limit = self.RATE_LIMIT_AUTHENTICATED

            elif not authenticated:
                rate_limit = self.RATE_LIMIT_PUBLIC

            else:
                return JsonResponse({'detail': 'Some thing is wrong. Try again later.'}, status=429)

        # Check if the request is allowed within the rate limit
        allowed = self.is_request_allowed(user_id, rate_limit)

        # If the request exceeds the rate limit, return an error
        if not allowed:
            return JsonResponse({'detail': 'Rate limit exceeded. Try again later.'}, status=429)

        # User is authenticated, proceed with the request
        return None

    def is_request_allowed(self, user_id, rate_limit):
        # Track api call counts based on user
        identifier = f'Ratelimit:u:{user_id}'
        request_count = cache.get(identifier, 0)

        if request_count >= rate_limit:
            return False

        # Increment request count in cache with timeout
        request_count += 1
        cache.set(identifier, request_count, timeout=self.RATE_LIMIT_DURATION)
        return True