import numpy as np

def modulus_between_values(value, min, max):
    diff = max - min
    while value < min:
        value += diff
    while value > max:
        value -= diff
    return value

def sigmoid(x, c=1):
  return 1 / (1 + np.exp(-c * x))