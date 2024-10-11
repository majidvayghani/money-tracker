# transactions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import NotFound


from ...models import Transaction
from .serializers import TransactionSerializer
from .permissions import IsProfileOwner

class TransactionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        List all transactions for the authenticated user's profile.
        """
        transactions = Transaction.objects.filter(_profile=request.user.profile)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new transaction linked to the authenticated user's profile.
        """
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_object(self, pk):
        """
        Helper method to get the transaction object associated with the authenticated user's profile.
        """
        # ToDo: Is it necessary to check the permission here again?
        return get_object_or_404(Transaction, _id=pk)

    def is_deleted(self, object):
        """
            verify if the object has been deleted.
            object can be any of project models
        """
        if object.deleted_at is None:
            return False
        
        # transaction is deleted
        return True
            

    def get(self, request, pk):
        """
        Retrieve a specific transaction by `_id`.
        """
        transaction = self.get_object(pk)
        self.check_object_permissions(request, transaction) 
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        """
            Step 0: Find the transaction.
            Step 1: Check whether the transaction is deleted or not.
            Step 2: If Step 1 passes, then update the transaction.
        """
        transaction = self.get_object(pk)
        self.check_object_permissions(request, transaction)
        if self.is_deleted(transaction):
            # Return a 404 response if the transaction is deleted
            raise NotFound(detail="Transaction not found.")
        else:
            serializer = TransactionSerializer(transaction, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        """
            Step 0: Find the transaction.
            Step 1: Check whether the transaction is deleted or not.
            Step 2: If Step 1 passes, then delete the transaction.
        """
        transaction = self.get_object(pk)
        self.check_object_permissions(request, transaction)

        if self.is_deleted(transaction):
            # Return a 404 response if the transaction is deleted
            raise NotFound(detail="Transaction not found.")
        else:
            transaction.deleted_at = timezone.now()
            transaction.save()
            return Response({"message": "transaction is deleted"}, status=status.HTTP_202_ACCEPTED)
        