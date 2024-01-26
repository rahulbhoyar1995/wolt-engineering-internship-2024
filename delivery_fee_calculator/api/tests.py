from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class CalculateDeliveryFeeTestCase(TestCase):
    """
    Test case class for the CalculateDeliveryFee API endpoint.
    """

    def setUp(self):
        """
        Set up method to initialize common attributes for tests.
        """
        self.client = APIClient()

    def test_calculate_delivery_fee_success_1(self):
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
        
        
    def test_calculate_delivery_fee_success_2(self):
        """
        Test a successful calculation of delivery fee.
        """
        data = {
            'cart_value': 910,
            'delivery_distance': 1780,
            'number_of_items': 17,
            'time': '2024-01-15T13:00:00Z',
        }

        response = self.client.post('', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['delivery_fee'], 1260)

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

    def test_calculate_delivery_fee_friday_rush_1(self):
        """
        Test the Friday rush scenario where the delivery fee is multiplied by 1.2x.
        """
        friday_rush_time = "2024-01-19T16:00:00Z"  # 4 PM UTC
        data = {
            'cart_value': 1500,
            'delivery_distance': 1000,
            'number_of_items': 4,
            'time': friday_rush_time,
        }

        response = self.client.post('', data, format='json')

        expected_fee = int(round(0 + 200 + 0) * 1.2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['delivery_fee'], expected_fee)
          
    def test_calculate_delivery_fee_friday_rush_2(self):
        """
        Test the Friday rush scenario where the delivery fee is multiplied by 1.2x.
        """
        friday_rush_time = "2024-02-02T17:00:00Z"  # 5 PM UTC
        data = {
            'cart_value': 2200,
            'delivery_distance': 1800,
            'number_of_items': 9,
            'time': friday_rush_time,
        }

        response = self.client.post('', data, format='json')

        expected_fee = int(round(0 + 400 + 250) * 1.2)
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

        expected_fee = int((1000 - 890) + round(200 + 0))
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

    def test_calculate_delivery_fee_invalid_input_distance(self):
        """
        Test with invalid input data: distance in string.
        """
        data = {
            'cart_value': 'invalid_value',
            'delivery_distance': "23432",
            'number_of_items': 4,
            'time': '2024-01-15T13:00:00Z',
        }

        response = self.client.post('', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)  # Check for validation error

    def test_calculate_delivery_fee_invalid_input_cart_value(self):
        """
        Test with invalid input data: cart value.
        """
        data = {
            'cart_value': 'invalid_value',
            'delivery_distance': 1000,
            'number_of_items': 4,
            'time': '2024-01-15T13:00:00Z',
        }

        response = self.client.post('', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_calculate_delivery_fee_invalid_input_time_value(self):
        """
        Test with invalid input data: time value.
        """
        data = {
            'cart_value': 3233,
            'delivery_distance': 1000,
            'number_of_items': 4,
            'time': 'incorrect',
        }

        response = self.client.post('', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_invalid_empty_data_request(self):
        """
        Test with invalid empty data in the request body.
        """
        invalid_data = {}
        response = self.client.post('', data=invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_from_request = str(response.data[0])
        expected_error = 'Bad Request. No input data provided. Please provide the input data in the request body.'
        self.assertEqual(error_from_request, expected_error)
