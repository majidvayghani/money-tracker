from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from accounts.models import CustomUser
from .serializers import UserSerializer

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        CustomUser.objects.create_user(
            email = serializer.validated_data['email'],
            password = serializer.validated_data['password']
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
