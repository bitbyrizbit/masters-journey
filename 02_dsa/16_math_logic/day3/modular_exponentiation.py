def mod_pow(b, e, m):
    if m == 1:
        return 0
    res = 1
    b = b % m
    while e > 0:
        if e & 1:
            res = (res * b) % m
        b = (b * b) % m
        e >>= 1
    return res
