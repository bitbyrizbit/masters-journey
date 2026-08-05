import collections

class MyCalendarThree:
    def __init__(self):
        # A dictionary to track the 'delta' or change in active bookings at each time point
        self.delta = collections.Counter()

    def book(self, start: int, end: int) -> int:
        """
        Adds the event and returns the maximum number of concurrent bookings (K-booking).
        """
        # Event starts -> concurrency increases by 1
        self.delta[start] += 1
        # Event ends -> concurrency decreases by 1
        self.delta[end] -= 1
        
        active = 0
        max_active = 0
        
        # Sweep-line: process all event points chronologically
        for time in sorted(self.delta.keys()):
            active += self.delta[time]
            if active > max_active:
                max_active = active
                
        return max_active
