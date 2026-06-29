s = "ADOBECODEBANC"
t = "ABC"

def min_window(s, t):
    target = [0] * 128
    for char in t:
        target[ord(char)] += 1
    missing = len(t)
    start = 0
    ans_start = 0
    min_len = float('inf')
    for end in range(len(s)):
        right_char = ord(s[end])
        if target[right_char] > 0:
            missing -= 1
        target[right_char] -= 1
        while missing == 0:
            if (end - start + 1) < min_len:
                min_len = end - start + 1
                ans_start = start
            left_char = ord(s[start])
            target[left_char] += 1
            if target[left_char] > 0:
                missing += 1
            start += 1
    return s[ans_start : ans_start + min_len] if min_len != float('inf') else ""

print(min_window(s, t))
