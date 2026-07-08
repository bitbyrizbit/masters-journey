import heapq

class Solution:
    def smallestRange(self,nums):
        min_heap = []
        cur_max = float('-inf')
        
        for i in range(len(nums)):
            heapq.heappush(min_heap, (nums[i][0], i, 0))
            cur_max = max(cur_max, nums[i][0])
        
        res = [float('-inf'), float('inf')]
        
        while len(min_heap) == len(nums):
            cur_min, list_idx, elem_idx = heapq.heappop(min_heap)
            if cur_max - cur_min < res[1] - res[0]:
                res = [cur_min, cur_max]
            if elem_idx + 1 < len(nums[list_idx]):
                next_val = nums[list_idx][elem_idx + 1]
                heapq.heappush(min_heap, (next_val, list_idx, elem_idx + 1))
                cur_max = max(cur_max, next_val)
        return res

sol = Solution()
print(sol.smallestRange([[4,10,15,24,26], [0,9,12,20], [5,18,22,30]]))
