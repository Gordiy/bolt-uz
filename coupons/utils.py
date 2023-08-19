"""Utils for coupons app."""

def is_integer(s: str) -> bool:
    """Check if string is integer."""
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(s: str) -> bool:
    """Check if string is float."""
    try:
        float(s)
        return True
    except ValueError:
        return False
