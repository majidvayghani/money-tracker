from django.contrib.auth import login, authenticate 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer

user = get_user_model()

@api_view(['POST'])
def create_user(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        password1 = serializer.validated_data['password1']
        
        try:
            if password != password1:
                return Response({'error': 'password dosent matched!'}, status=status.HTTP_400_BAD_REQUEST)
            
            user.objects.create_user(
                email = email,
                password = password
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as er:
            return Response({"error": f"Failed to create user: {str(er)}"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            # get the user from the database
            user = user.objects.get(email=email)

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