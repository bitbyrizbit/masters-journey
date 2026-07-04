import heapq

class Solution:
    def kClosest(self,points,k):
        max_heap = []
        for x, y in points:
            dist = x**2 + y**2
            heapq.heappush(max_heap, (-dist, [x, y]))
            if len(max_heap) > k:
                heapq.heappop(max_heap)
        return [point for dist, point in max_heap]


sol = Solution()
print(sol.kClosest([[1,3],[-2,2]],1))
