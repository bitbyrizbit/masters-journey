s = "abdcabcbb"

def substring(s):
    if not s:
        return 0
    first = 0 
    second = 1
    max_length = 1
    while second < len(s):
        if s[second] not in s[first:second]:
            current_length = second - first + 1
            max_length = max(max_length, current_length)
        else:
            first += 1
            second -= 1
        second += 1
    return max_length
print(substring(s))