import collections

class MyCalendarThree:
    def __init__(self):
        self.d = collections.Counter()

    def book(self, start, end):
        self.d[start] += 1
        self.d[end] -= 1
        
        cur = mx = 0
        for t in sorted(self.d.keys()):
            cur += self.d[t]
            if cur > mx:
                mx = cur
                
        return mx
