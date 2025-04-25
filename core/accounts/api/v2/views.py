from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
import logging

from .serializers import *
from tokens.models import Token
from tokens.authentication import CustomTokenAuthentication
from .rabbitmq import send_log_message, send_email_message

logger = logging.getLogger('account')
User = get_user_model()

class SignupAPIview(APIView):
    def post(self, request, *args, **kwargs):
        """
        Handle user signup.
        """
        logger.info("Received signup request: %s", request.data)
        serializer = SignupSerializer(data=request.data)
        queue = "signup_queue"
        
        if serializer.is_valid():
            user = serializer.save()
            data = serializer.data

            send_email_message(queue, data)
            logger.info("User signup successful: %s", user.email)
            send_log_message(data)

            return Response({
                'user': serializer.data,
            }, status=status.HTTP_201_CREATED)

        logger.debug("Signup request validation failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SigninAPIview(APIView):
    def post(self, request, *args, **kwargs):
        """
        Handle user login, validate credentials, and issue token.
        """
        logger.info("Received signin request for user: %s", request.data.get('email'))

        serializer = SigninSerializer(data=request.data)

        if not serializer.is_valid():
            email = request.data.get('email')
            errors = serializer.errors
            logger.warning("Signin failed for user: %s. Errors: %s", email, errors)
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']

        try:
            token, created = Token.objects.get_or_create(_user=user, is_active=True)
            logger.info("Signin successful for user: %s", user.email)
            return Response({
                'token': token.token,
                'email': user.email,
                'created': created
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                "Error during signin process for user: %s. Exception: %s",
                user.email,
                str(e))
            return Response({'message': 'An error occurred during signin.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SignoutAPIView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        """
        Handle user signout.
        """
        logger.info("Received signout request: %s", request.data)
        serializer = SignoutSerializer(data={}, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            logger.info("User signed out successfully")
            return Response({'message': 'Signout successful.'}, status=status.HTTP_200_OK)

        logger.error(
            "Error during signout process. Exception: %s", str(e))
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)