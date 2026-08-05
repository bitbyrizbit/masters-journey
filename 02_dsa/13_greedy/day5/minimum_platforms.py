"""
Minimum Number of Platforms Required (GFG Classic / FAANG Variant)

Problem:
    Given arrival and departure times of trains at a railway station, find the
    minimum number of platforms required so that no train waits.

Approach (Sweep Line / Two-Pointer):
    1. Sort arrivals and departures independently.
    2. Use two pointers — one for arrivals, one for departures.
    3. If the next train arrives before the earliest-departing train leaves,
       increment platform count (need a new platform).
    4. Otherwise the departing train frees a platform → decrement.
    5. Track the peak count across the sweep.

    This is equivalent to Meeting Rooms II but uses the two-pointer variant
    instead of a heap, achieving O(1) extra space after sorting.

Complexity:
    Time:  O(N log N) — dominated by sorting two arrays
    Space: O(N)       — sorting copies (or O(1) if sorted in-place)
"""

from typing import List


def find_platform_count(arrivals: List[int], departures: List[int]) -> int:
    n = len(arrivals)
    if n == 0:
        return 0

    arrivals.sort()
    departures.sort()

    platforms = 0
    max_platforms = 0
    i = 0  # pointer into arrivals
    j = 0  # pointer into departures

    while i < n and j < n:
        if arrivals[i] <= departures[j]:
            # A new train arrives before the earliest-departing train leaves
            platforms += 1
            max_platforms = max(max_platforms, platforms)
            i += 1
        else:
            # A train departs — a platform becomes free
            platforms -= 1
            j += 1

    return max_platforms


# ── Tests ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        # (arrivals, departures, expected)
        ([900, 940, 950, 1100, 1500, 1800],
         [910, 1200, 1120, 1130, 1900, 2000], 3),

        ([100, 200, 300],
         [150, 250, 350], 1),   # sequential, never overlap

        ([100, 100, 100],
         [200, 200, 200], 3),   # all arrive at the same time

        ([900],
         [910], 1),             # single train

        ([], [], 0),             # edge: empty
    ]

    for arrivals, departures, expected in test_cases:
        result = find_platform_count(arrivals[:], departures[:])
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] arrivals={arrivals} -> {result} (expected {expected})")
