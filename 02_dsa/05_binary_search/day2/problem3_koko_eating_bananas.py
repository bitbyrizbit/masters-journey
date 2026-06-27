import math

def minEatingSpeed(piles, h):
    low = 1
    high = max(piles)
    while low < high:
        mid = (low + high) // 2
        total_hours = 0
        for pile in piles:
            total_hours += math.ceil(pile / mid)
        if total_hours <= h:
            high = mid
        else:
            low = mid + 1
    return low

piles = [3,6,7,11]
h = 8
print(minEatingSpeed(piles,h))