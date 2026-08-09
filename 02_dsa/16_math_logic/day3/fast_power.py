def my_pow(x, n):
    if n < 0:
        x = 1 / x
        n = -n
    res = 1
    cur = x
    while n > 0:
        if n & 1:
            res *= cur
        cur *= cur
        n >>= 1
    return res
