from django.contrib.auth import login, authenticate 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, LoginSerializer

User = get_user_model()


def create_user(data):
    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    raise serializer.errors

@api_view(['POST'])
def signup(request):
    try: 
        data = create_user(request.data)
        return Response(data, status=status.HTTP_201_CREATED)
    except Exception as er:
        return Response({"error": str(er)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def signin(request):
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

