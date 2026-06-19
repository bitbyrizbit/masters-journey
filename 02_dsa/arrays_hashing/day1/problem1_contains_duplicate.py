# Brute approach
def contains_duplicate_brute(arr):
    unique = []  
    for i in arr:
        if i in unique:
            return True
        unique.append(i)
    return False
print(contains_duplicate_brute([1,2,3,4]))

# Set conversion 
def contains_duplicate_set(arr):
    unique = set(arr)
    if len(unique) != len(arr): return True
    return False
print(contains_duplicate_set([1,2,3]))

# Early-exit optimized   
def contains_duplicate_optimized(arr):
    seen = set()
    for x in arr:
        if x in seen:
            return True
        seen.add(x)
    return False
print(contains_duplicate_optimized([1,2,3]))