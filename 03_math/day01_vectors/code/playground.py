"""
Vector Playground
Do not treat this as production code. This is a mathematical laboratory.
"""

v1 = [1,2]
v2 = [3,4,6]
v3 = [5,6,7]
v4 = [1]

def add_vectors(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Vectors must be of the same length")
    return [v1[i] + v2[i] for i in range(len(v1))]

def subtract_vectors(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Vectors must be of the same length")
    return [v1[i] - v2[i] for i in range(len(v1))]

def dot_product(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Vectors must be of the same length")
    return sum(v1[i] * v2[i] for i in range(len(v1)))

def scalar_multiply(scalar, v):
    return [scalar * v[i] for i in range(len(v))]

def vector_length(v):
    return sum(x**2 for x in v) ** 0.5

def normalize_vector(v):
    length = vector_length(v)
    if length == 0:
        raise ValueError("Cannot normalize a zero-length vector")
    return [x / length for x in v]

def distance_between_vectors(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Vectors must be of the same length")
    return vector_length(subtract_vectors(v1, v2))

# print("Addition of v1 and v2:", add_vectors(v1, v2))
# print("Subtraction of v1 and v2:", subtract_vectors(v1, v2))
# print("Dot product of v1 and v2:", dot_product(v1, v2))
# print("Scalar multiplication of 2 and v1:", scalar_multiply(2, v1))
# print("Length of v1:", vector_length(v1))
# print("Normalization of v1:", normalize_vector(v1))
# print("Distance between v1 and v2:", distance_between_vectors(v1, v2))

# print("Addition of v1 and v3:", add_vectors(v1, v3))
# print("Subtraction of v1 and v3:", subtract_vectors(v1, v3))
# print("Dot product of v1 and v3:", dot_product(v1, v3))
# print("Scalar multiplication of 3 and v3:", scalar_multiply(3, v3))
# print("Length of v3:", vector_length(v3))
# print("Normalization of v3:", normalize_vector(v3))
# print("Distance between v1 and v3:", distance_between_vectors(v1, v3))

print("Addition of v2 and v3:", add_vectors(v2, v3))
print("Subtraction of v2 and v3:", subtract_vectors(v2, v3))
print("Dot product of v2 and v3:", dot_product(v2, v3))
print("Scalar multiplication of 4 and v4:", scalar_multiply(4, v4))
print("Length of v4:", vector_length(v4))
print("Normalization of v4:", normalize_vector(v4))
print("Distance between v2 and v3:", distance_between_vectors(v2, v3))