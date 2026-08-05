"""
Bag of Tokens (LeetCode 948)

Problem:
    You start with some power and 0 score.
    You have tokens where token[i] has value tokens[i].
    Operations:
      - Face up (spend):  if power >= tokens[i], spend tokens[i] power to gain 1 score.
      - Face down (gain): if score >= 1, spend 1 score to gain tokens[i] power.
    Maximise your score.

Approach (Two-Pointer Greedy):
    Sort tokens.
    Use two pointers: lo = cheapest token, hi = most expensive token.
    - If we can afford tokens[lo], buy it (gain score). lo++.
    - Otherwise, if we have score to spare and more tokens remain, sell the
      most expensive token (tokens[hi]) to gain power. hi--.
    - If neither is possible, stop.
    Track the maximum score seen throughout (not just at the end, since
    selling score for power might lower the score but allow future buys).

Proof (Greedy Stays Ahead):
    When buying, we always buy the cheapest available (minimise power cost per
    score point). When selling, we always sell the most expensive (maximise
    power gained per score point). Any deviation increases cost or decreases
    benefit at each step, which can only reduce the final maximum score.

Complexity:
    Time:  O(N log N) — sort, then O(N) two-pointer sweep
    Space: O(1)       — constant extra space
"""

from typing import List


def bag_of_tokens_score(tokens: List[int], power: int) -> int:
    tokens.sort()
    lo, hi = 0, len(tokens) - 1
    score = 0
    max_score = 0

    while lo <= hi:
        if power >= tokens[lo]:
            # Spend power to gain score — always buy cheapest
            power -= tokens[lo]
            score += 1
            max_score = max(max_score, score)
            lo += 1
        elif score > 0:
            # Sell most expensive token to gain power
            power += tokens[hi]
            score -= 1
            hi -= 1
        else:
            # Can't buy and can't sell — game over
            break

    return max_score


# ── Tests ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        ([100], 50, 0),              # can't afford; no score to sell → 0
        ([100, 200], 150, 1),        # buy 100 → score=1; can't buy 200 → 1
        ([100, 200, 300, 400], 200, 2),  # buy 100(p=100), buy 200? No. sell 400(p=500), buy 200(p=300,s=1), buy 300(p=0,s=2) → max=2
        ([], 100, 0),                # edge: no tokens
        ([71, 55, 82], 54, 0),       # can't afford cheapest (55 > 54), no score → 0
    ]

    for tokens, power, expected in test_cases:
        result = bag_of_tokens_score(tokens[:], power)
        status = "PASS" if result == expected else "FAIL"
        print(f"[{status}] tokens={tokens}, power={power} -> {result} (expected {expected})")
