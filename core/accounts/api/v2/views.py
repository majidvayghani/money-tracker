from django.contrib.auth import login, authenticate 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer, AuthTokenSerializer

User = get_user_model()

@api_view(['POST'])
def create_user_v1(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        password1 = serializer.validated_data['password1']

        try:
            if password != password1:
                return Response({'error': 'password dosent matched!'}, status=status.HTTP_400_BAD_REQUEST)
            
            User.objects.create_user(
                email = email,
                password = password
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as er:
            return Response({"error": f"Failed to create user: {str(er)}"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_user(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        try: 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as er:
            return Response({"error": f"Failed to create user: {str(er)}"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user_v1(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            # get the user from the database
            user = User.objects.get(email=email)

            if not user.is_active:
                return Response({"error": "Account is inactive."}, status=status.HTTP_403_FORBIDDEN)

            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return Response({"error": "Login successful"}, status=status.HTTP_200_OK)
            else:
                # If the password is incorrect
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        except user.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_401_UNAUTHORIZED)

    # If validation fails (e.g., missing or malformed data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })