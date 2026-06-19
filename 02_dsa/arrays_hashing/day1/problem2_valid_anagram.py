from collections import Counter

def anagram(s,t):
    return Counter(s) == Counter(t)
print(anagram("listen","silent"))


def anagram_subtraction(s, t):
    if len(s) != len(t):
        return False
    return not (Counter(s) - Counter(t))
print(anagram_subtraction("listen", "listennn"))
