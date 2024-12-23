import logging
from django.http import JsonResponse

logger = logging.getLogger('core')

class CustomAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 401:
            logger.error("Unauthorized access attempt. Invalid token.")

        return response
