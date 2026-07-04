import heapq

class KthLargest:
    def __init__(self,k,nums):
        self.k = k
        self.min_heap = []
        for num in nums:
            self.add(num)
    
    def add(self,val):
        heapq.heappush(self.min_heap, val)
        if len(self.min_heap) > self.k:
            heapq.heappop(self.min_heap)
        return self.min_heap[0]


kthLargest = KthLargest(3,[4,5,8,2])
print(kthLargest.add(3))
print(kthLargest.add(5))
print(kthLargest.add(10))
print(kthLargest.add(9))
print(kthLargest.add(4))