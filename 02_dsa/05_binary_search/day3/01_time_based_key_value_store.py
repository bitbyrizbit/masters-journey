store = {}

def set(key, value, timestamp):
    if key not in store:
        store[key] = []
    store[key].append([timestamp, value])

def get(key, timestamp):
    if key not in store:
        return ""
    pairs = store[key]
    left, right = 0, len(pairs) - 1
    res = ""
    while left <= right:
        mid = (left + right) // 2
        if pairs[mid][0] <= timestamp:
            res = pairs[mid][1]
            left = mid + 1
        else:
            right = mid - 1            
    return res

print(set("foo", "bar", 1))
print(get("foo", 1))
print(get("foo", 3))
print(set("foo", "bar2", 4))
print(get("foo", 4))
print(get("foo", 5))