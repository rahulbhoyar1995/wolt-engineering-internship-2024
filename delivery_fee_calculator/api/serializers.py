"""
delivery_fee_calculator/serializers.py
Serializers for the Delivery Fee Calculator application.

This module defines serializers used for handling data related to delivery fees.

Classes:
    - DeliveryFeeCalculatorSerializer: Serializer for the delivery fee response.

Author:
    Rahul Bhoyar

Date:
    January 24, 2024
"""

from rest_framework import serializers

class DeliveryFeeCalculatorSerializer(serializers.Serializer):
    """
    Serializer for the delivery fee response.

    This serializer is responsible for validating and serializing data related to the delivery fee response.
    It includes a single field:
        - delivery_fee: An integer field representing the calculated delivery fee in cents.

    Usage:
        To use this serializer, instantiate it with data to be validated and call the `is_valid()` method.
        If the data is valid, access the validated data using the `data` attribute.

    Example:
        serializer = DeliveryFeeCalculatorSerializer(data={'delivery_fee': 1000})
        if serializer.is_valid():
            print(serializer.data['delivery_fee'])  # Access the validated delivery_fee value.

    Attributes:
        - delivery_fee: Integer field representing the calculated delivery fee in cents.

    Methods:
        - validate_delivery_fee(value): Custom validation method for the 'delivery_fee' field.

    Raises:
        - serializers.ValidationError: Raised when validation fails.
    """

    delivery_fee = serializers.IntegerField()

    def validate_delivery_fee(self, value):
        """
        Custom validation method for the 'delivery_fee' field.

        Args:
            - value (int): The value to be validated.

        Returns:
            - int: The validated value.

        Raises:
            - serializers.ValidationError: Raised if the value is invalid.
        """
        # Add custom validation logic here if needed.
        return value
