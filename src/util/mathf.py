def modulus_between_values(value, min, max):
    diff = max - min
    while value < min:
        value += diff
    while value > max:
        value -= diff
    return value