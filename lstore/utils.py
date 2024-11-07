def set_bit(value, bit_position):
    """Sets the bit at the given position to 1."""
    return value | (1 << bit_position)

def clear_bit(value, bit_position):
    """Clears the bit at the given position to 0."""
    return value & (~(1 << bit_position))

def toggle_bit(value, bit_position):
    """Toggles the bit at the given position."""
    return value ^ (1 << bit_position)

def get_bit(value, bit_position):
    """Returns the value of the bit at the given position."""
    return (value >> bit_position) & 1

