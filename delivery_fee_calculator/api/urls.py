"""
Delivery Fee Calculator URL Configuration.

This module defines the URL patterns for the Delivery Fee Calculator application.

Attributes:
    urlpatterns (list): A list of URL patterns for mapping views to specific endpoints.

Example:
    To include these patterns in your project's main URL configuration, use the 'include' function:

    ```python
    from django.urls import include, path

    urlpatterns = [
        path('delivery-fee/', include('delivery_fee_calculator.urls')),
        # ... other URL patterns for your project
    ]
    ```

URL Patterns:
    - An empty path ('') maps to the `CalculateDeliveryFee` view, which calculates the delivery fee based on the provided input.

    Usage example:
    ```python
    from django.urls import path
    from .views import CalculateDeliveryFee

    urlpatterns = [
        path('', CalculateDeliveryFee.as_view(), name='calculate_delivery_fee'),
    ]
    ```
"""

from django.urls import path
from .views import CalculateDeliveryFee

urlpatterns = [
    path('', CalculateDeliveryFee.as_view(), name='calculate_delivery_fee'),
]
