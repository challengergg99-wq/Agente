def create_phone_number(n):
    """
    Create a phone number from a list of integers.

    Args:
        n (list): A list of 10 integers.
    """
    # Convert the list of integers to a string
    phone_number = ''.join(map(str, n))
    
    # Format the phone number
    formatted_number = f"({phone_number[:3]}) {phone_number[3:6]}-{phone_number[6:]}"
    
    return formatted_number