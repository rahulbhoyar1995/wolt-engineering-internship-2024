from django.urls import path
from .views import CalculateDeliveryFee

urlpatterns = [
    path('', CalculateDeliveryFee.as_view(), name='calculate_delivery_fee'),
]