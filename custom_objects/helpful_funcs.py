import math

def vector_magnitude(vector):
    return math.sqrt((vector[0]**2) + (vector[1]**2))

def unit_vector(vector):
    magnitude = vector_magnitude(vector)
    return ((vector[0] / magnitude), (vector[1] / magnitude))