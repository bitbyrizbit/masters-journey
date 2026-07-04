import heapq

class MedianFinder:
    def __init__(self):
        self.small = []
        self.large = []
    
    def addNum(self,num):
        heapq.heappush(self.small,-num)
        if self.small and self.large and (-self.small[0] > self.large[0]):
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def findMedian(self):
        if len(self.small) > len(self.large):
            return float(-self.small[0])
        return (-self.small[0] + self.large[0]) / 2.0


median = MedianFinder()
median.addNum(1)
median.addNum(2)
print(median.findMedian())
median.addNum(3)
print(median.findMedian())