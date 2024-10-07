from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from transactions.models import Transaction
from .serializers import TransactionSerializer


User = get_user_model()

class TransactionDetail(APIView):
    """
        Retrieve, Update or Delete a transaction
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Transaction.objects.get(pk=pk)
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def get_object_foreign_key(self, pk):
        try:
            return self.get_object(pk)._user_id
        except Exception as er:
            return Response({"error": str(er)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction)        

        # ToDo: change permission
        if User.get_user_id_by_email(request.user) != serializer.data['_user']:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        if User.get_user_by_email(request.user).deleted_at == None:
            return Response({"message": "transaction is already deleted"}, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        serializer = TransactionSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        transaction = self.get_object(pk)
        # it's not a good idea because an attacker can find the ID pattern.
        if (transaction.deleted_at != None):
            return Response({"message": "transaction is already deleted"}, status=status.HTTP_200_OK)
        
        if transaction:
            transaction.deleted_at = timezone.now()
            transaction.save()
            return Response({"message": "transaction is deleted"}, status=status.HTTP_202_ACCEPTED)
        
    def put(self, request, pk):
        transaction = self.get_object(pk)
        serializer = TransactionSerializer(transaction, data = request.data)

        if User.get_user_id_by_email(request.user) != self.get_object_foreign_key(pk):
            return Response({"message": "Permission is Denied!!!"}, status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)