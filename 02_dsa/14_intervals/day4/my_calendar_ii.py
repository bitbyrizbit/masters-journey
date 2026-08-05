class MyCalendarTwo:
    def __init__(self):
        self.cal = []
        self.overlaps = []

    def book(self, start, end):
        for s, e in self.overlaps:
            if start < e and s < end:
                return False
                
        for s, e in self.cal:
            if start < e and s < end:
                self.overlaps.append((max(start, s), min(end, e)))
                
        self.cal.append((start, end))
        return True
