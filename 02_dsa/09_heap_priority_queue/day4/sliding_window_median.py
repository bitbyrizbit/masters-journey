import heapq
import collections

class Solution:
    def medianSlidingWindow(self,nums,k):
        small, large = [], []
        lazy = collections.Counter()
        
        def balance():
            while small and lazy[-small[0]]:
                lazy[-small[0]] -= 1
                heapq.heappop(small)
            while large and lazy[large[0]]:
                lazy[large[0]] -= 1
                heapq.heappop(large)
            if len(small) > len(large) + 1:
                heapq.heappush(large, -heapq.heappop(small))
                balance()
            elif len(large) > len(small):
                heapq.heappush(small, -heapq.heappop(large))
                balance()
        
        for i in range(k):
            heapq.heappush(small, -nums[i])
        
        for _ in range(k // 2):
            heapq.heappush(large, -heapq.heappop(small))
        res = []
        
        if k % 2 == 1:
            res.append(float(-small[0]))
        else:
            res.append((-small[0] + large[0]) / 2.0)
        
        for i in range(k, len(nums)):
            out_num = nums[i - k]
            in_num = nums[i]
            lazy[out_num] += 1
            balance()
            balance_diff = -1 if out_num <= -small[0] else 1
            if in_num <= -small[0]:
                balance_diff += 1
                heapq.heappush(small, -in_num)
            else:
                balance_diff -= 1
                heapq.heappush(large, in_num)
            if balance_diff > 0:
                heapq.heappush(large, -heapq.heappop(small))
            elif balance_diff < 0:
                heapq.heappush(small, -heapq.heappop(large))
            balance()
            if k % 2 == 1:
                res.append(float(-small[0]))
            else:
                res.append((-small[0] + large[0]) / 2.0)
        return res

sol = Solution()
print(sol.medianSlidingWindow([1,3,-1,-3,5,3,6,7], 3))