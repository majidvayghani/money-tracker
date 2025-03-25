from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound
import logging

from ...models import Profile
from .serializers import *
from .rabbitmq import send_log_message, send_email_message

logger = logging.getLogger('account')
User = get_user_model()

class SignupAPIview(APIView):
    def post(self, request, *args, **kwargs):
            logger.info("Received signup request: %s", request.data)
            serializer = SignupSerializer(data=request.data)
            queue = "signup_queue"

            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                logger.info("User signup successful: %s", data)

                send_email_message(queue, data)
                logger.info("Email sent to queue: %s", queue)

                send_log_message(data)
                logger.info("Log message sent for data: %s", data)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
            logger.debug("Signup request validation failed: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SigninAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        logger.info("Received signin request: %s", request.data['email'])
        user = User.get_user_by_email(request.data['email'])
        if (user is None) or (user.deleted_at):
            logger.error('User not found!')
            return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = SigninAuthTokenSerializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            logger.error("Signin failed. errors: %s", str(serializer.errors))
            raise e
        # ToDo: send user_id to Token
        user_email = serializer.validated_data['user']
        try:
            token, created = Token.objects.get_or_create(user=user_email)
        except Exception as e:
            logger.debug("Failed to create or retrieve token for user: %s. error: %s", user.email, str(e))
            
        logger.info("Signin successfully for user: %s", request.data['email'])
        return Response({
            'token': token.key,
            'email': user.email,
            'created': created,
        })
  
class SignoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            logger.info("User signed out successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error("Error during user signout for %s", str(e))

class UserGetOrUpdateOrDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """
            change password or email
        """
        return Response({"message": "To Do"}, status=status.HTTP_302_FOUND)


    def delete(self, request, *args, **kwargs):
        return Response({"message": "User cannot be deleted"}, status=status.HTTP_403_FORBIDDEN)

class ProfileGetOrUpdateOrDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]


    def is_deleted(self, object):
        """
            verify if the object has been deleted.
        """
        if object.deleted_at is None:
            return False
        # Object is deleted
        return True

    def get_object(self):
        user = self.request.user
        try:
            return Profile.objects.get(_user=user)
        except Profile.DoesNotExist:
            raise NotFound("Profile not found for the current user.")

    def get(self, request):
        profile = self.get_object()

        if self.is_deleted(profile):
            raise NotFound(detail="Profile not found.")
        else:
            serializer = ProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        profile = self.get_object()
        if self.is_deleted(profile):
            raise NotFound(detail="Profile not found.")
        else:
            serializer = ProfileSerializer(profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = self.get_object()  # Get the user's profile
        profile.deleted_at = timezone.now()
        profile.save()  # save the profile
        return Response(status=status.HTTP_204_NO_CONTENT)