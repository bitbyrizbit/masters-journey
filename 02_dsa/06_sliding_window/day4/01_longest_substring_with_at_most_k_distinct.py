def distinct_substring(s,k):
    if not s or k == 0:
        return 0
    char_map = {}
    left = 0
    max_length = 0
    for right in range(len(s)):
        char_map[s[right]] = char_map.get(s[right], 0) + 1
        while len(char_map) > k:
            char_map[s[left]] -= 1
            if char_map[s[left]] == 0:
                del char_map[s[left]]
            left += 1
        max_length = max(max_length, right - left + 1)
    return max_length

s = "eceba"
k = 2
print(distinct_substring(s,k))
