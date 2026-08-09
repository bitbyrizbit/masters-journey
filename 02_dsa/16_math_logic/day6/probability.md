# Probability in Algorithms

Probability is the measure of the likelihood that an event will occur. In coding interviews, probability problems often intersect with Dynamic Programming.

## 1. Classical Probability
If all outcomes are equally likely, the probability of an event $A$ is:
$P(A) = \frac{\text{Number of favorable outcomes}}{\text{Total number of possible outcomes}}$

## 2. Independent Events
If two events $A$ and $B$ are independent (one does not affect the outcome of the other):
$P(A \cap B) = P(A) \cdot P(B)$

## 3. Expected Value
The Expected Value $E[X]$ is the long-run average value of a random variable $X$.
$E[X] = \sum x_i \cdot P(x_i)$

### Expected Value Linearity
A crucial property of Expected Value is **Linearity**:
$E[X + Y] = E[X] + E[Y]$
This holds true even if the variables $X$ and $Y$ are dependent!

## 4. Probability DP (State Transition)
For problems involving a sequence of probabilistic choices (e.g. Knight Probability on Chessboard), we define a DP table:
`dp[k][r][c]` = probability of being at cell `(r, c)` after `k` moves.

The transition is:
`dp[k][r][c] = sum(dp[k-1][prev_r][prev_c] * P(transition_from_prev))`
