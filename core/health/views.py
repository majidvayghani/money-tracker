from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PingView(APIView):
    """
    A simple view to test if the API is responsive.
    """
    def get(self, request, format=None):
        return Response({"message": "pong"}, status=status.HTTP_200_OK)