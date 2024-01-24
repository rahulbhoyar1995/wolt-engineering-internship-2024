# delivery_fee_calculator/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DeliveryFeeCalculatorSerializer
from .utils import delivery_fee_calculation

class CalculateDeliveryFee(APIView):
    """
    API endpoint to calculate the delivery fee based on the provided input.

    Request Payload:
    {
        "cart_value": Integer,  # Value of the shopping cart in cents
        "delivery_distance": Integer,  # Distance between the store and customer's location in meters
        "number_of_items": Integer,  # Number of items in the customer's shopping cart
        "time": String  # Order time in UTC in ISO format
    }

    Response Payload:
    {
        "delivery_fee": Integer  # Calculated delivery fee in cents
    }
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to calculate the delivery fee.

        Args:
        - request: HTTP request object
        - args: Additional positional arguments
        - kwargs: Additional keyword arguments

        Returns:
        - Response: HTTP response object
        """
        # Extract input data from the request
        cart_value = request.data.get('cart_value')
        delivery_distance = request.data.get('delivery_distance')
        number_of_items = request.data.get('number_of_items')
        time = request.data.get('time')
        
        print("Type cart value:", type(cart_value))
        # Calculate the delivery fee using the utility function
        delivery_fee = delivery_fee_calculation(cart_value, delivery_distance, number_of_items, time)

        # Prepare the response data
        data = {'delivery_fee': delivery_fee}

        # Serialize the response data
        serializer = DeliveryFeeCalculatorSerializer(data=data)

        # Check if the serialization is valid
        if serializer.is_valid():
            # Return the serialized data in the response
            return Response(serializer.data)
        else:
            # Return an error response if serialization fails
            return Response(serializer.errors, status=400)
