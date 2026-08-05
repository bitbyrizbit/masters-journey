class MyCalendar:
    def __init__(self):
        # We will store a list of non-overlapping intervals
        self.calendar = []

    def book(self, start: int, end: int) -> bool:
        """
        Returns True if the event can be booked without causing a double booking.
        """
        # Check against all existing events for overlap
        for s, e in self.calendar:
            # Condition for overlap: start1 < end2 AND start2 < end1
            if start < e and s < end:
                return False
                
        # No overlaps found, we can safely book it
        self.calendar.append((start, end))
        return True
