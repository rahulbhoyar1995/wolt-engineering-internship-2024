def validate_time_format(time):
    from datetime import datetime
    try:
        datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False

def validate_input_data(cart_value, delivery_distance, number_of_items, time):
    if not all(isinstance(val, int) for val in [cart_value, delivery_distance, number_of_items]) or not isinstance(time, str):
        return False
    if any(val < 0 for val in [cart_value, delivery_distance, number_of_items]):
        return False
    if not validate_time_format(time):
        return False
    return True

def calculate_surcharge_for_lower_cart_value_order(cart_value):
    minimum_cart_value = 1000
    surcharge = max(0, minimum_cart_value - cart_value)
    return surcharge

def calculate_surcharge_for_large_orders(num_items):
    item_surcharge_threshold = 4
    bulk_fee_threshold = 12
    item_surcharge = max(0, (num_items - item_surcharge_threshold) * 50)
    bulk_fee = 120 if num_items > bulk_fee_threshold else 0

    total_surcharge = item_surcharge + bulk_fee
    return total_surcharge

def calculate_delivery_fee_in_cents_for_distance(distance):
    base_fee_cents = 200
    additional_fee_per_500m_cents = 100

    if distance <= 1000:
        return base_fee_cents

    # Calculate additional fees for each 500 meters beyond the first kilometer
    additional_distance = max(0, distance - 1000)  # Distance beyond the first kilometer

    if additional_distance % 500 == 0:
        additional_fee_cents = (additional_distance // 500) * additional_fee_per_500m_cents
    else:
        additional_fee_cents = ((additional_distance // 500) + 1) * additional_fee_per_500m_cents

    # Add additional fees to the base fee
    delivery_fee_cents = base_fee_cents + additional_fee_cents

    return delivery_fee_cents


def friday_rush_multiplier(delivery_fee,time):
    from datetime import datetime
    FRIDAY_RUSH_START = 15  # 3 PM in 24-hour format
    FRIDAY_RUSH_END = 19  # 7 PM in 24-hour format
    FRIDAY_RUSH_MULTIPLIER = 1.2

    order_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
    if order_time.weekday() == 4 and FRIDAY_RUSH_START <= order_time.hour < FRIDAY_RUSH_END:
        delivery_fee = delivery_fee * FRIDAY_RUSH_MULTIPLIER
        return delivery_fee 
    else:
        return delivery_fee
        

def delivery_fee_calculation(cart_value, delivery_distance, number_of_items, time):
    if cart_value >= 20000:
        return 0
    # Step 1
    surcharge_for_lower_cart_value_order = calculate_surcharge_for_lower_cart_value_order(cart_value)
    #print("surcharge_for_lower_cart_value_order :",surcharge_for_lower_cart_value_order)

    # Step 2
    delivery_fee_in_cents_for_distance = calculate_delivery_fee_in_cents_for_distance(delivery_distance)
    #print("delivery_fee_in_cents_for_distance :",delivery_fee_in_cents_for_distance)

    # Step 3
    surcharge_for_large_orders = calculate_surcharge_for_large_orders(number_of_items)
    #print("surcharge_for_large_orders :",surcharge_for_large_orders)
    
    total_delivery_fee = surcharge_for_lower_cart_value_order + delivery_fee_in_cents_for_distance + surcharge_for_large_orders 

    #Step 4 : Friday rush case
    total_delivery_fee = int(friday_rush_multiplier(total_delivery_fee,time))

    if total_delivery_fee > 1500:
        return 1500

    return total_delivery_fee