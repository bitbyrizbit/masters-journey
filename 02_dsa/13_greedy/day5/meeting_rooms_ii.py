"""
Meeting Rooms II (LeetCode 253)

Problem:
    Given an array of meeting time intervals [start, end], find the minimum
    number of conference rooms required to hold all meetings simultaneously.

Approach:
    Use a Min-Heap tracking end times of rooms in use.
    - Sort meetings by start time.
    - For each meeting, if the earliest-ending room finishes before this meeting
      starts, reuse it (pop from heap). Then push this meeting's end time.
    - The heap size at the end equals the peak simultaneous meetings.

Complexity:
    Time:  O(N log N) — sort + N heap operations each O(log N)
    Space: O(N)       — heap can hold all meetings in the worst case
"""

import heapq
from typing import List


def min_meeting_rooms(intervals: List[List[int]]) -> int:
    if not intervals:
        return 0

    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    # Min-heap of end times of currently occupied rooms
    heap: List[int] = []

    for start, end in intervals:
        # If the earliest-ending room is free before this meeting starts, reuse it
        if heap and heap[0] <= start:
            heapq.heapreplace(heap, end)   # pop earliest, push new end
        else:
            heapq.heappush(heap, end)      # need a new room

    return len(heap)


# ── Tests ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([[0, 30], [5, 10], [15, 20]], 2),   # [0,30] clashes with both others
        ([[7, 10], [2, 4]],            1),   # sequential after sort
        ([],                            0),   # edge: empty
        ([[1, 5], [2, 3], [3, 8]],     2),   # [1,5] and [2,3] clash
        ([[1, 4], [2, 5], [7, 9]],     2),   # [1,4] and [2,5] clash; [7,9] reuses
    ]

    for intervals, expected in test_cases:
        result = min_meeting_rooms(intervals)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] intervals={intervals} -> {result} (expected {expected})")
