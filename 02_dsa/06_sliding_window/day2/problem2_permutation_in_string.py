from collections import Counter

s1 = "ab"
s2 = "eidbaooo"

def permutation(s1, s2):
    k = len(s1)
    target = Counter(s1)
    window = Counter(s2[:k])
    for i in range(k, len(s2)):
        if target == window:
            return True
        window[s2[i]] += 1
        left_char = s2[i - k]
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]            
    return target == window

print(permutation(s1, s2))
