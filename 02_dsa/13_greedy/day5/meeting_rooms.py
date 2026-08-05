"""
Meeting Rooms (LeetCode 252)

Problem:
    Given an array of meeting time intervals [start, end], determine if a person
    could attend all meetings (i.e., no two meetings overlap).

Approach:
    Sort intervals by start time. For any two consecutive meetings, if the end
    time of the earlier meeting exceeds the start time of the next, they overlap.

Complexity:
    Time:  O(N log N) — dominated by sort
    Space: O(1)       — constant extra space (or O(N) if sort is not in-place)
"""

from typing import List


def can_attend_meetings(intervals: List[List[int]]) -> bool:
    # Sort by start time
    intervals.sort(key=lambda x: x[0])

    for i in range(1, len(intervals)):
        # If the current meeting starts before the previous one ends → overlap
        if intervals[i][0] < intervals[i - 1][1]:
            return False

    return True


# ── Tests ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([[0, 30], [5, 10], [15, 20]], False),   # overlap at [0,30] and [5,10]
        ([[7, 10], [2, 4]],            True),    # no overlap after sorting
        ([],                            True),    # edge: empty → trivially true
        ([[1, 5]],                      True),    # edge: single meeting
        ([[1, 2], [2, 3]],             True),    # adjacent (touch, not overlap)
    ]

    for intervals, expected in test_cases:
        result = can_attend_meetings(intervals)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] intervals={intervals} -> {result} (expected {expected})")
