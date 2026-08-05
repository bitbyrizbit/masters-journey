"""
Candy (LeetCode 135)

Problem:
    N children stand in a line. Each child has a rating.
    Distribute candies such that:
      1. Every child must receive at least one candy.
      2. A child with a higher rating than its immediate neighbor gets more candies.
    Return the minimum total candies required.

Approach (Two-Pass Greedy):
    Pass 1 (Left → Right):
        Give each child 1 candy. If child[i] has a higher rating than child[i-1],
        give child[i] exactly one more candy than child[i-1].
        This satisfies the left-neighbor constraint.

    Pass 2 (Right → Left):
        If child[i] has a higher rating than child[i+1], ensure child[i] has at
        least one more candy than child[i+1]. Take the max of current and required.
        This satisfies the right-neighbor constraint.

    Sum all candy counts.

Proof (Two-Pass Correctness):
    After Pass 1, every left-neighbor constraint is satisfied.
    Pass 2 only increases candy counts — it never violates left-neighbor constraints
    because we take the max (we never decrease a count set by Pass 1).
    After Pass 2, all right-neighbor constraints are also satisfied.
    Taking the max at each step ensures we don't over-correct either direction.

    This is not greedy in the "single decision" sense — it is a two-pass scan where
    each pass greedily satisfies one directional constraint. Together they are both
    necessary and sufficient for optimality.

Complexity:
    Time:  O(N) — two linear passes
    Space: O(N) — candy array
"""

from typing import List


def candy(ratings: List[int]) -> int:
    n = len(ratings)
    if n == 0:
        return 0

    candies = [1] * n

    # Pass 1: Left → Right
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1

    # Pass 2: Right → Left
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)

    return sum(candies)


# ── Tests ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([1, 0, 2], 5),           # child 0 gets 2, child 1 gets 1, child 2 gets 2
        ([1, 2, 2], 4),           # child 0→1, child 1→2, child 2→1 (not strictly greater)
        ([1, 3, 4, 5, 2], 11),    # ascending then drop: 1,2,3,4,1 → corrected to 1,2,3,4,2 → sum=12? let's check
        ([1], 1),                  # single child
        ([1, 2, 3, 4, 5], 15),    # strictly ascending: 1,2,3,4,5
        ([5, 4, 3, 2, 1], 15),    # strictly descending: 5,4,3,2,1
    ]

    for ratings, expected in test_cases:
        result = candy(ratings)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] ratings={ratings} -> {result} (expected {expected})")
