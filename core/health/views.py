from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connections
from django.db.utils import OperationalError
from redis.exceptions import ConnectionError
import redis

class PingView(APIView):
    """ A simple view to check the status of critical components """

    def get(self, request):
        # Initialize the status dictionary
        status = {'status': 'healthy'}

        # Database Check
        try:
            db_conn = connections['default']
            db_conn.cursor()
            if not db_conn.is_usable():  # Check if the database is usable
                raise OperationalError('Database not usable')
        except OperationalError:
            status['database'] = 'down'
            status['status'] = 'unhealthy'
        else:
            status['database'] = 'up'

        # Redis Check
        try:
            client = redis.Redis(host='redis', port=6379)
            client.ping()
            status['redis'] = 'up'
        except ConnectionError:
            status['redis'] = 'down'
            status['status'] = 'unhealthy'

        # Return response based on status
        if status['status'] == 'unhealthy':
            return Response(status, status=500)
        
        return Response(status)