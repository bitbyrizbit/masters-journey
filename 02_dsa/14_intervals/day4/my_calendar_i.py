class MyCalendar:
    def __init__(self):
        self.cal = []

    def book(self, start, end):
        for s, e in self.cal:
            if start < e and s < end:
                return False
        self.cal.append((start, end))
        return True
