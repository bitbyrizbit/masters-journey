import heapq

class Solution:
    def findMaximizedCapital(self,k,w,profits,capital):
        projects = sorted(zip(capital,profits))
        max_heap = []
        i = 0
        n = len(projects)
        for j in range(k):
            while i < n and projects[i][0] <= w:
                heapq.heappush(max_heap, -projects[i][1])
                i += 1
            if not max_heap:
                break
            w += -heapq.heappop(max_heap)
        return w


sol = Solution()
print(sol.findMaximizedCapital(2,0,[1,2,3],[0,1,1]))
