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
from .cache_key import get_transaction_key as generator

User = get_user_model()

class TransactionDetail(APIView):
    """
        Retrieve, Update or Delete a transaction
    """
    permission_classes = [IsAuthenticated]

    def is_deleted(self, object):
        """
            verify if the object has been deleted.
            object can be any of project models
        """
        if object.deleted_at is None:
            return object

        raise NotFound(detail="Object is already deleted(soft!).")
        
    def get_object_from_db(self, transaction_id, key):
        """
            retrieve transaction from DB and cache it
        """
        try:
            transaction = Transaction.objects.get(pk=transaction_id)
            if self.is_deleted(transaction):
                cache.set(key, transaction)
                return transaction
            else:
                # Return a 404 response if the transaction is not found
                raise NotFound(detail="Transaction not found.")
            
        except Transaction.DoesNotExist:
            raise NotFound(detail="Transaction not found.")

    def get_object_from_cache(self, key):
        """
            retrieve transaction from cache 
        """
        return cache.get(key)

    def get(self, request, pk, format=None):
        """
            generate cache key and use it in get_object_from_cache and get_object_from_db 
            cache key always is unique because user_id and transaction_id are unique
            first try to retrieve object from cache
            get_object_from_db will raise a NotFound exception if the transaction does not exist
        """ 
        key = generator(request.user._id, pk)
        transaction = self.get_object_from_cache(key)

        if transaction is not None:
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            """
                The transaction hasn't been cached
            """
            transaction = self.get_object_from_db(pk, key)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        # ToDo: create a method for this
        # if User.get_user_id_by_email(request.user) != serializer.data['_user']:
        #     return Response(status=status.HTTP_403_FORBIDDEN)
        
    def post(self, request):
        serializer = TransactionSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():
            transaction = serializer.save()
            key = generator(request.user._id, transaction._id)
            cache.set(key, transaction)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        key = generator(request.user._id, pk)
        transaction = self.get_object_from_cache(key)
        if transaction.deleted_at is None:
            transaction.deleted_at = timezone.now()
            transaction.save()
            cache.delete(key)
            return Response({"message": "transaction is deleted(soft!)"}, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)