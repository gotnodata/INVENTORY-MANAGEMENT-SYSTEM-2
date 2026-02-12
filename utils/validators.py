import config


def validate_username(username):
    """Validate username"""
    if not username or not username.strip():
        return False, "Username cannot be empty"
    return True, ""


def validate_password(password):
    """Validate password"""
    if not password:
        return False, "Password cannot be empty"
    if len(password) < config.MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {config.MIN_PASSWORD_LENGTH} characters"
    return True, ""


def validate_item_data(name, category, quantity, price):
    """Validate item data"""
    if not name or not name.strip():
        return False, "Item name is required"
    if not category or not category.strip():
        return False, "Category is required"
    try:
        int(quantity)
    except ValueError:
        return False, "Quantity must be a number"
    try:
        float(price)
    except ValueError:
        return False, "Price must be a number"
    return True, ""


def validate_quantity(quantity):
    """Validate quantity input"""
    if quantity is None:
        return False, "Quantity cannot be empty"
    try:
        int(quantity)
        return True, ""
    except ValueError:
        return False, "Quantity must be a valid number"


def validate_price(price):
    """Validate price input"""
    if price is None:
        return False, "Price cannot be empty"
    try:
        float(price)
        return True, ""
    except ValueError:
        return False, "Price must be a valid number"
