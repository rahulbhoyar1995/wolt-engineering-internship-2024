"""
Tests for the CalculateDeliveryFee API endpoint.
"""

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta

class CalculateDeliveryFeeTestCase(TestCase):
    """
    Test case class for the CalculateDeliveryFee API endpoint.
    """

    def setUp(self):
        """
        Set up method to initialize common attributes for tests.
        """
        self.client = APIClient()

    def test_calculate_delivery_fee_success(self):
        """
        Test a successful calculation of delivery fee.
        """
        data = {
            'cart_value': 790,
            'delivery_distance': 2235,
            'number_of_items': 4,
            'time': '2024-01-15T13:00:00Z',
        }

        response = self.client.post('', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['delivery_fee'], 710)

    def test_calculate_delivery_fee_free_delivery(self):
        """
        Test when the cart value is equal or more than 200€, the delivery is free.
        """
        data = {
            'cart_value': 20000,  # 200€ in cents
            'delivery_distance': 1500,
            'number_of_items': 5,
            'time': '2024-01-15T13:00:00Z',
        }

        response = self.client.post('', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['delivery_fee'], 0)

    def test_calculate_delivery_fee_friday_rush(self):
        """
        Test the Friday rush scenario where the delivery fee is multiplied by 1.2x.
        """
        friday_rush_time = datetime.utcnow().replace(hour=16, minute=0, second=0)  # 4 PM UTC

        data = {
            'cart_value': 1500,
            'delivery_distance': 1000,
            'number_of_items': 4,
            'time': friday_rush_time.strftime('%Y-%m-%dT%H:%M:%SZ'),
        }

        response = self.client.post('', data, format='json')

        expected_fee = int(round(2 + 1 + 50 + 120) * 1.2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['delivery_fee'], expected_fee)

    def test_calculate_delivery_fee_small_order_surcharge(self):
        """
        Test the scenario where a small order surcharge is added.
        """
        data = {
            'cart_value': 890,
            'delivery_distance': 1000,
            'number_of_items': 4,
            'time': '2024-01-15T13:00:00Z',
        }

        response = self.client.post('', data, format='json')

        expected_fee = int(round(2 + 1 + 50 + 120) + (1000 - 890))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['delivery_fee'], expected_fee)

    def test_calculate_delivery_fee_maximum_fee_constraint(self):
        """
        Test the scenario where the delivery fee cannot be more than 15€.
        """
        data = {
            'cart_value': 10000,
            'delivery_distance': 10000,
            'number_of_items': 15,
            'time': '2024-01-15T13:00:00Z',
        }

        response = self.client.post('', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['delivery_fee'], 1500)

    def test_calculate_delivery_fee_invalid_input(self):
        """
        Test with invalid input data.
        """
        data = {
            'cart_value': 'invalid_value',
            'delivery_distance': 1000,
            'number_of_items': 4,
            'time': '2024-01-15T13:00:00Z',
        }

        response = self.client.post('', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cart_value', response.data)  # Check for validation error

    # Add more test cases as needed based on specific scenarios.
