def mySqrt(x):
    if x < 2:
        return x 
    low = 1
    high = x // 2  
    ans = 0
    while low <= high:
        mid = low + (high - low) // 2
        num = mid * mid
        if num == x:
            return mid
        elif num < x:
            ans = mid      
            low = mid + 1  
        else:
            high = mid - 1             
    return ans

print(mySqrt(4))  
print(mySqrt(8))  
print(mySqrt(0))  
