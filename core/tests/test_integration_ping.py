from django.test import TestCase, Client
import pytest

class PingEndpointIntegrationTest(TestCase):
    """
    Integration tests for the /api/ping endpoint.
    """

    def setUp(self):
        """
        Initialize the test client.
        """
        self.client = Client()
        self.url = 'http://127.0.0.1:8000/ping'

    @pytest.mark.integration
    def test_ping_endpoint_success(self):
        """
        Test that a GET request to ping endpoint returns a 200 status and 'pong' message.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'pong'})
    @pytest.mark.integration
    def test_ping_endpoint_method_not_allowed(self):
        """
        Test that a POST request to ping endpoint returns a 405 Method Not Allowed.
        """
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 405)
  
