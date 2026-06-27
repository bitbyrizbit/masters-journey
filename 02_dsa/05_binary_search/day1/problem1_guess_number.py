def guess(num):
    if num > pick:
        return -1
    elif num < pick:
        return 1
    else:
        return 0

def guess_number(n: int) -> int:
    low = 1
    high = n
    while low <= high:
        mid = (low + high) // 2
        res = guess(mid)
        
        if res == 0:
            return mid
        elif res == -1:
            high = mid - 1
        else:
            low = mid + 1 
    return -1

n = 10
pick = 6
print(guess_number(n)) 
