from datetime import datetime

def validate_time_format(time):
    """
    Validate the format of the input time string.

    Args:
        time (str): Input time string.

    Returns:
        bool: True if the time is in the correct format, False otherwise.
    """
    try:
        datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False

def validate_input_data(cart_value, delivery_distance, number_of_items, time):
    """
    Validate input data for cart, delivery distance, number of items, and time.

    Args:
        cart_value (int): Cart value.
        delivery_distance (int): Delivery distance.
        number_of_items (int): Number of items in the cart.
        time (str): Order time.

    Returns:
        bool: True if input data is valid, False otherwise.
    """
    if not all(isinstance(val, int) for val in [cart_value, delivery_distance, number_of_items]) or not isinstance(time, str):
        return False
    if any(val < 0 for val in [cart_value, delivery_distance, number_of_items]):
        return False
    if not validate_time_format(time):
        return False
    return True

def calculate_surcharge_for_lower_cart_value_order(cart_value):
    """
    Calculate surcharge for lower cart value orders.

    Args:
        cart_value (int): Cart value.

    Returns:
        int: Surcharge amount.
    """
    minimum_cart_value = 1000
    surcharge = max(0, minimum_cart_value - cart_value)
    return surcharge

def calculate_surcharge_for_large_orders(num_items):
    """
    Calculate surcharge for large orders based on the number of items.

    Args:
        num_items (int): Number of items in the cart.

    Returns:
        int: Surcharge amount.
    """
    item_surcharge_threshold = 4
    bulk_fee_threshold = 12
    item_surcharge = max(0, (num_items - item_surcharge_threshold) * 50)
    bulk_fee = 120 if num_items > bulk_fee_threshold else 0

    total_surcharge = item_surcharge + bulk_fee
    return total_surcharge

def calculate_delivery_fee_in_cents_for_distance(distance):
    """
    Calculate delivery fee in cents based on the delivery distance.

    Args:
        distance (int): Delivery distance.

    Returns:
        int: Delivery fee in cents.
    """
    base_fee_cents = 200
    additional_fee_per_500m_cents = 100

    if distance <= 1000:
        return base_fee_cents

    additional_distance = max(0, distance - 1000)
    if additional_distance % 500 == 0:
        additional_fee_cents = (additional_distance // 500) * additional_fee_per_500m_cents
    else:
        additional_fee_cents = ((additional_distance // 500) + 1) * additional_fee_per_500m_cents

    delivery_fee_cents = base_fee_cents + additional_fee_cents
    return delivery_fee_cents

def friday_rush_multiplier(delivery_fee, time):
    """
    Apply a rush multiplier to the delivery fee on Fridays during rush hours.

    Args:
        delivery_fee (int): Original delivery fee.
        time (str): Order time.

    Returns:
        int: Updated delivery fee after applying the rush multiplier.
    """
    friday_rush_start= 15
    friday_rush_end = 19
    friday_rush_multiplier = 1.2

    order_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    if order_time.weekday() == 4 and friday_rush_start<= order_time.hour < friday_rush_end:
        delivery_fee = delivery_fee * friday_rush_multiplier
        return delivery_fee
    else:
        return delivery_fee

def delivery_fee_calculation(cart_value, delivery_distance, number_of_items, time):
    """
    Calculate the total delivery fee based on input parameters.

    Args:
        cart_value (int): Cart value.
        delivery_distance (int): Delivery distance.
        number_of_items (int): Number of items in the cart.
        time (str): Order time.

    Returns:
        int: Total calculated delivery fee.
    """
    if cart_value >= 20000:
        return 0

    surcharge_for_lower_cart_value_order = calculate_surcharge_for_lower_cart_value_order(cart_value)
    delivery_fee_in_cents_for_distance = calculate_delivery_fee_in_cents_for_distance(delivery_distance)
    surcharge_for_large_orders = calculate_surcharge_for_large_orders(number_of_items)

    total_delivery_fee = surcharge_for_lower_cart_value_order + delivery_fee_in_cents_for_distance + surcharge_for_large_orders

    total_delivery_fee = int(friday_rush_multiplier(total_delivery_fee, time))

    if total_delivery_fee > 1500:
        return 1500

    return total_delivery_fee
