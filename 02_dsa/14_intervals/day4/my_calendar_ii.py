class MyCalendarTwo:
    def __init__(self):
        # Stores all normal bookings
        self.calendar = []
        # Stores exclusively the overlapping regions (double bookings)
        self.overlaps = []

    def book(self, start: int, end: int) -> bool:
        """
        Returns True if the event can be booked without causing a triple booking.
        """
        # Step 1: Check against known double bookings.
        # If the new event overlaps with an existing overlap, it creates a triple booking!
        for s, e in self.overlaps:
            if start < e and s < end:
                return False
                
        # Step 2: The booking is valid. 
        # Now we must record any NEW double bookings it creates with existing single events.
        for s, e in self.calendar:
            if start < e and s < end:
                # The overlap region is max(starts) to min(ends)
                self.overlaps.append((max(start, s), min(end, e)))
                
        # Step 3: Add the valid event to the main calendar
        self.calendar.append((start, end))
        return True
