def isBadVersion(version):
    return version >= bad

def firstBadVersion(n: int) -> int:
    low = 1
    high = n
    while low < high:
        mid = low + (high - low) // 2
        if isBadVersion(mid):
            high = mid 
        else:
            low = mid + 1 
    return low

bad = 4
print(firstBadVersion(5)) 
bad = 1
print(firstBadVersion(1))
bad = 2
print(firstBadVersion(7)) 
