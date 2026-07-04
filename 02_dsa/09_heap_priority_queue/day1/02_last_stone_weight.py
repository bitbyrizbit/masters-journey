import heapq

class Solution:
    def lastStoneWeight(self,stones):
        max_heap = [-s for s in stones]
        heapq.heapify(max_heap)
        while len(max_heap) > 1:
            stone1 = -heapq.heappop(max_heap)
            stone2 = -heapq.heappop(max_heap)
            if stone1 != stone2:
                heapq.heappush(max_heap, -(stone1 - stone2))
        return -max_heap[0] if max_heap else 0


sol = Solution()
print(sol.lastStoneWeight([2,7,4,1,8,1]))