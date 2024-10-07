from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import SigninAuthTokenSerializer, SignupSerializer, UserProfileSerializer

User = get_user_model()

class SignupAPIview(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("\n\n\n\n\n **************** errors: ", serializer.errors, "\n\n\n\n\n ****************")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SigninAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        user = User.get_user_by_email(request.data['email'])
        if user.deleted_at != None:
            return Response({'message' : 'User is Deleted!'}, status=status.HTTP_204_NO_CONTENT)

        serializer = SigninAuthTokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'email': user.email,
            'created': created,
        })
  
class SignoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserGetOrUpdateOrDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = User.get_user_by_email(request.user)
        if user:
            user.deleted_at = timezone.now()
            request.user.auth_token.delete()
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
