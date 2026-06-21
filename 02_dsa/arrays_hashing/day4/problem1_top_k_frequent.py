# Problem 1: Top K Frequent Elements

from collections import Counter

def top_k_frequent(nums, k):
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for num, frequency in counts.items():
        buckets[frequency].append(num)
    output_list = []
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            output_list.append(num)
            if len(output_list) == k:
                return output_list
nums = [1, 1, 1, 2, 2, 3]
k = 2
print(top_k_frequent(nums, k))

