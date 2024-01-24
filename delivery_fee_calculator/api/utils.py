from datetime import datetime

def delivery_fee_calculation(cart_value, delivery_distance, number_of_items, time):
    """
    Calculate the delivery fee based on input parameters.

    Args:
        cart_value (int): Value of the shopping cart in cents.
        delivery_distance (int): Distance between the store and customer's location in meters.
        number_of_items (int): Number of items in the customer's shopping cart.
        time (str): Order time in UTC in ISO format (e.g., "2024-01-15T13:00:00Z").

    Returns:
        int: Calculated delivery fee in cents.
    """
    # Constants
    SMALL_ORDER_SURCHARGE_THRESHOLD = 1000  # 10€ in cents
    BASE_DELIVERY_FEE = 200  # 2€ in cents
    ADDITIONAL_DISTANCE_FEE = 100  # 1€ in cents
    MIN_DISTANCE_FEE = ADDITIONAL_DISTANCE_FEE
    ITEM_SURCHARGE = 50  # 0.50€ in cents
    BULK_ITEM_SURCHARGE = 120  # 1.20€ in cents
    MAX_DELIVERY_FEE = 1500  # 15€ in cents
    FREE_DELIVERY_THRESHOLD = 20000  # 200€ in cents
    FRIDAY_RUSH_START = 15  # 3 PM in 24-hour format
    FRIDAY_RUSH_END = 19  # 7 PM in 24-hour format
    FRIDAY_RUSH_MULTIPLIER = 1.2

    # Calculate small order surcharge
    small_order_surcharge = max(0, SMALL_ORDER_SURCHARGE_THRESHOLD - cart_value)

    # Calculate base delivery fee
    delivery_fee = BASE_DELIVERY_FEE

    # Calculate additional distance fee
    additional_distance = max(0, delivery_distance - 1000)
    additional_distance_fee = ((additional_distance + MIN_DISTANCE_FEE - 1) // MIN_DISTANCE_FEE) * ADDITIONAL_DISTANCE_FEE

    # Calculate item surcharge
    item_surcharge = max(0, number_of_items - 4) * ITEM_SURCHARGE

    # Calculate bulk item surcharge
    bulk_item_surcharge = max(0, number_of_items - 12) * ITEM_SURCHARGE + BULK_ITEM_SURCHARGE

    # Calculate total surcharge
    total_surcharge = small_order_surcharge + additional_distance_fee + item_surcharge + bulk_item_surcharge

    # Check if it's Friday rush
    order_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    if order_time.weekday() == 4 and FRIDAY_RUSH_START <= order_time.hour < FRIDAY_RUSH_END:
        delivery_fee *= FRIDAY_RUSH_MULTIPLIER
        total_surcharge *= FRIDAY_RUSH_MULTIPLIER

    # Apply total surcharge to delivery fee
    delivery_fee += total_surcharge

    # Apply maximum delivery fee constraint
    delivery_fee = min(delivery_fee, MAX_DELIVERY_FEE)

    # Check for free delivery
    if cart_value >= FREE_DELIVERY_THRESHOLD:
        delivery_fee = 0

    return int(round(delivery_fee))  # Return in cents
