"""
Maximum Units on a Truck (LeetCode 1710)

Problem:
    You are assigned to put some amount of boxes onto one truck.
    boxTypes[i] = [numberOfBoxes, numberOfUnitsPerBox]
    The truck can carry at most `truckSize` boxes total.
    Maximise the total number of units on the truck.

Approach:
    Sort box types by units per box descending.
    Greedily fill the truck with boxes that carry the most units first.

Proof (Exchange Argument):
    If we pick a box with fewer units before a box with more units,
    swapping them increases (or maintains) total units. Therefore,
    always picking the highest units-per-box first is optimal.

Complexity:
    Time:  O(N log N) — dominated by sort
    Space: O(1)       — in-place sort, constant extra
"""

from typing import List


def maximum_units(box_types: List[List[int]], truck_size: int) -> int:
    # Sort by units per box descending (most valuable boxes first)
    box_types.sort(key=lambda x: x[1], reverse=True)

    total_units = 0
    remaining = truck_size

    for num_boxes, units_per_box in box_types:
        # Take as many boxes of this type as we can fit
        take = min(num_boxes, remaining)
        total_units += take * units_per_box
        remaining -= take

        if remaining == 0:
            break  # Truck is full

    return total_units


# ── Tests ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([[1, 3], [2, 2], [3, 1]], 4, 8),    # take 1×3 + 2×2 + 1×1 = 3+4+1 = 8
        ([[5, 10], [2, 5], [4, 7], [3, 9]], 10, 91),  # 10,9,7,5 sort → fill
        ([[1, 1]], 3, 1),                      # only 1 box available
        ([[3, 3], [3, 3]], 3, 9),              # pick 3 boxes of either type
        ([], 5, 0),                             # edge: no boxes
    ]

    for boxes, size, expected in test_cases:
        result = maximum_units([b[:] for b in boxes], size)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] boxes={boxes}, size={size} -> {result} (expected {expected})")
