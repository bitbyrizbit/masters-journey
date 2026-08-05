"""
IPO — Maximise Capital (LeetCode 502)

Problem:
    You have w initial capital and can complete at most k projects.
    Each project i has a capital requirement `capital[i]` and profit `profits[i]`.
    A project can only be started if you have at least `capital[i]` capital.
    After completing a project, its profit is added to your capital.
    Return the maximum capital after at most k projects.

Approach (Two-Heap Greedy):
    1. Min-Heap of (capital_required, profit) → tracks which projects we
       can afford as our capital grows.
    2. Max-Heap of profit → among all currently affordable projects, we
       always pick the one with the highest profit (greedy).

    Each round:
        - Push all newly affordable projects (capital[i] <= w) into the max-heap.
        - Pop the highest-profit project from the max-heap and complete it.
        - Repeat k times.

    The greedy choice "always pick the highest available profit" is optimal
    because completing a cheaper alternative project first can only increase
    our future affordable set — but if we could complete the highest-profit
    affordable project now, doing so adds the most capital to unlock future projects.

Complexity:
    Time:  O(N log N + k log N) — sorting + k heap pops
    Space: O(N)                 — two heaps together hold at most N projects
"""

import heapq
from typing import List


def find_maximised_capital(k: int, w: int, profits: List[int], capital: List[int]) -> int:
    n = len(profits)

    # Min-heap: (capital_required, profit) — sorted by capital requirement
    min_heap = sorted(zip(capital, profits))   # sort once; treat as a sorted queue
    min_idx = 0

    # Max-heap: negate profits since Python's heapq is a min-heap
    max_heap: List[int] = []

    for _ in range(k):
        # Unlock all projects we can now afford
        while min_idx < n and min_heap[min_idx][0] <= w:
            cap, prof = min_heap[min_idx]
            heapq.heappush(max_heap, -prof)    # negate for max-heap behaviour
            min_idx += 1

        if not max_heap:
            break  # No affordable project exists → stop early

        # Complete the most profitable affordable project
        w += -heapq.heappop(max_heap)

    return w


# ── Tests ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        # (k, w, profits, capital, expected)
        (2, 0, [1, 2, 3], [0, 1, 1], 4),       # 0→pick p=1(cap0)→w=1, pick p=3(cap1)→w=4
        (3, 0, [1, 2, 3], [0, 1, 2], 6),       # pick all three in order of profit
        (1, 0, [1, 2, 3], [1, 1, 2], 0),       # can't afford any with w=0
        (2, 1, [1, 2, 3], [1, 1, 2], 6),       # pick p=2(cap1)→w=3, then p=3(cap2)→w=6
        (0, 5, [10, 20], [1, 2], 5),            # k=0, no projects → return initial w
    ]

    for k, w, profits, capital, expected in test_cases:
        result = find_maximised_capital(k, w, profits[:], capital[:])
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] k={k}, w={w} -> {result} (expected {expected})")
