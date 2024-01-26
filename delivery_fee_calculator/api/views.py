from json.decoder import JSONDecodeError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, ValidationError
from .serializers import DeliveryFeeCalculatorSerializer
from .utils import delivery_fee_calculation, validate_input_data

class CalculateDeliveryFee(APIView):
    """
    API endpoint to calculate the delivery fee based on the provided input.
    The request should be a POST request with the input data in the request body.

    Request Payload:
    {
        "cart_value": Integer - Value of the shopping cart in cents
        "delivery_distance": Integer - Distance between the store and customer's location in meters
        "number_of_items": Integer - Number of items in the customer's shopping cart
        "time": String - Order time in UTC in ISO format
    }

    Response Payload:
    {
        "delivery_fee": Integer - Calculated delivery fee in cents
    }
    """

    def post(self, request, *args, **kwargs):
        try:
            # Check if request data is empty
            if not request.data:
                raise ValidationError(detail='Bad Request. No input data provided. Please provide the input data in the request body.')

            # Extract input data from the request
            cart_value = request.data.get('cart_value')
            delivery_distance = request.data.get('delivery_distance')
            number_of_items = request.data.get('number_of_items')
            time = request.data.get('time')

            # Validate input data
            if not validate_input_data(cart_value, delivery_distance, number_of_items, time):
                # Return an error response if validation fails
                error = {'error': 'Invalid input data. Please ensure that all input values are provided and in the correct format.'}
                return Response(error, status=400)

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
        except JSONDecodeError:
            # Handle JSON parse error
            raise ParseError(detail='Invalid JSON format. Please provide a valid JSON.')
