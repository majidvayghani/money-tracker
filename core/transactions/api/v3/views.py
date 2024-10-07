from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.exceptions import NotFound

from transactions.models import Transaction
from .serializers import TransactionSerializer


User = get_user_model()

class TransactionDetail(APIView):
    """
        Retrieve, Update or Delete a transaction
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        pk = str(pk)  # Ensure pk is a string
        transaction = cache.get(pk)

        if transaction is None:
            """
                The transaction hasn't been cached
            """
            try:
                # retrieve transaction from DB and cache it
                transaction = Transaction.objects.get(pk=pk)
                cache.set(pk, transaction)
                return transaction
            except Transaction.DoesNotExist:
                # Return a 404 response if the transaction is not found
               raise NotFound(detail="Transaction not found.")

        return transaction

    def get(self, request, pk, format=None):
       # get_object will raise a NotFound exception if the transaction does not exist
        transaction = self.get_object(pk)

        serializer = TransactionSerializer(transaction)

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    

    def post(self, request):
        serializer = TransactionSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            transaction = serializer.save()
            transaction.pk = str(transaction.pk)
            cache.set(transaction.pk, transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
