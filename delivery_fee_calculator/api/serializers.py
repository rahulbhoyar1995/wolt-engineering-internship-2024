from rest_framework import serializers

class DeliveryFeeCalculatorSerializer(serializers.Serializer):
    delivery_fee = serializers.IntegerField()
