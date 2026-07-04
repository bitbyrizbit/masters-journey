import collections
import heapq

class Solution:
    def topKFrequent(self,nums,k):
        count = collections.Counter(nums)
        min_heap = []
        for num, freq in count.items():
            heapq.heappush(min_heap, (freq, num))
            if len(min_heap) > k:
                heapq.heappop(min_heap)
        return [num for freq, num in min_heap]


sol = Solution()
print(sol.topKFrequent([1,1,1,2,2,3],2))
