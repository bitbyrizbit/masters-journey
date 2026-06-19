anagrams = ["eat","tea","tan","ate","nat","bat"]

"""
First attempt (Incorrect approach - intentionally preserved)

Idea:
    Assign each alphabet a number:
    a=1, b=2, c=3, ...
Then compute the sum of character values for each word and use that sum as the grouping key.

Why it seemed valid:
    Anagrams contain same letters, so their sums match.

Why it fails:
    Different non-anagram words can also produce the same sum (hash collision).
    
Example:
"ad" -> 1 + 4 = 5
"bc" -> 2 + 3 = 5

These are not anagrams but get grouped together.

Lesson: 
    When designing hash keys/signatures, always test collision cases.
"""

# ----- Failed Attempt Preserved for Learning -----
alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_dict = {}
for i in range(len(alphabet)):
    alphabet_dict[alphabet[i]] = i + 1    
def group_anagrams(anagrams):
    group = {}
    for word in anagrams:
        count = 0
        for letter in word:
            count += alphabet_dict[letter]
        if count not in group:
            group[count] = []
        group[count].append(word)
    return group
print(group_anagrams(anagrams))


# ----- Correct Solution -----
def group_anagrams_optimized(anagrams):
    groups = {}
    for word in anagrams:
        signature = "".join(sorted(word))
        
        if signature not in groups:
            groups[signature] = []
        groups[signature].append(word)
    return list(groups.values())
print(group_anagrams_optimized(anagrams))