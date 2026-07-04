import collections
import heapq

class Solution:
    def leastInterval(self,tasks,n):
        count = collections.Counter(tasks)
        max_heap = [-cnt for cnt in count.values()]
        heapq.heapify(max_heap)
        time = 0
        cooldown_queue = collections.deque()
        while max_heap or cooldown_queue:
            time += 1
            if max_heap:
                cnt = heapq.heappop(max_heap) + 1
                if cnt != 0:
                    cooldown_queue.append((cnt, time + n))
            if cooldown_queue and cooldown_queue[0][1] == time:
                heapq.heappush(max_heap, cooldown_queue.popleft()[0])
        return time


sol = Solution()
print(sol.leastInterval(["A","A","A","B","B","B"],2))
