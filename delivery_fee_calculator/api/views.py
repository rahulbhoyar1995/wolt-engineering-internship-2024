# delivery_fee_calculator/views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import DeliveryFeeCalculatorSerializer
from django.utils import timezone
from .utils import delivery_fee_calculation



class CalculateDeliveryFee(APIView):
    def post(self, request, *args, **kwargs):
        cart_value = request.data.get('cart_value')
        delivery_distance = request.data.get('delivery_distance')
        number_of_items = request.data.get('number_of_items')
        time = request.data.get('time')

        # Perform the delivery fee calculation based on the specifications
        # ...

        # Create and save a DeliveryFeeCalculator instance
        delivery_fee = delivery_fee_calculation(cart_value,delivery_distance,number_of_items,time)
        data = {'delivery_fee': delivery_fee}
        serializer = DeliveryFeeCalculatorSerializer(data=data)

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
