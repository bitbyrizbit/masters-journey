"""
Vector Basics

Goal: Implement fundamental vector operations manually using Python lists.

Restrictions:
- No NumPy
- No numpy.linalg
- No math.dist
- No numpy.dot
"""

def add(a, b):
    for i in range(len(a)):
        a[i] += b[i]
    return a

def subtract(a, b):
    for i in range(len(a)):
        a[i] -= b[i]
    return a

def scalar_multiply(c, v):
    for i in range(len(v)):
        v[i] *= c
    return v

def magnitude(v):
    sum_of_squares = 0
    for i in range(len(v)):
        sum_of_squares += v[i] ** 2
    return sum_of_squares ** 0.5

def normalize(v):
    mag = magnitude(v)
    if mag == 0:
        raise ValueError("Cannot normalize the zero vector")
    return scalar_multiply(1 / mag, v)

def distance(a, b):
    diff = subtract(a.copy(), b)
    return magnitude(diff)

v1 = [3, 4]
v2 = [1, 2]

print("Vector v1:", v1)
print("Vector v2:", v2)
print("v1 + v2:", add(v1.copy(), v2))
print("v1 - v2:", subtract(v1.copy(), v2))
print("2 * v1:", scalar_multiply(2, v1))
print("Magnitude of v1:", magnitude(v1))
print("Normalized v1:", normalize(v1))
print("Distance between v1 and v2:", distance(v1, v2))