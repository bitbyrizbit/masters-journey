## Probability DP

* **Problem Type:** Expected Value Computation / State-Space Probability Propagation
* **Data Structure Used:** 2D or 3D DP array (state indexed by step, position)
* **Approach 1:** Brute-force simulation / Monte Carlo. Run the random process millions of times and average the outcomes. This gives an approximate answer but not an exact one, and it's computationally impractical for exact probability queries.
* **Optimized Approach:** Forward probability DP. Define `dp[r][c]` as the probability of being at position `(r, c)` at a given step. On each step, distribute the probability mass from each cell to all reachable next cells, weighted by the transition probability. Roll this forward exactly $K$ times.
* **Complexity:**
  * **Time:** $O(K \cdot N^2 \cdot M)$ where $K$ is steps, $N \times N$ is the board size, and $M$ is the number of possible moves per cell (8 for a knight).
  * **Space:** $O(N^2)$ — only two DP layers (current and next) need to be stored at any time.
* **Pointer Flow:**
```text
Knight probability on a 3x3 board from (1,1) after 1 step:
Valid knight moves: (+-1, +-2), (+-2, +-1)
From (1,1): possible moves are (2,3),(2,-1),(0,3),(0,-1),(3,2),(-1,2),(3,0),(-1,0)
On a 3x3 board (indices 0..2), valid destinations:
 - (2, 3) out, (2, -1) out, (0, 3) out, (0, -1) out
 - (3, 2) out, (-1, 2) out, (3, 0) out, (-1, 0) out
All 8 moves leave the board! Probability remaining = 0.
```
```text
On a 5x5 board from (2,2) after 1 step:
dp[2][2] = 1.0 initially.
Each valid move gets probability += 1.0 / 8.0 = 0.125
Valid moves from (2,2): (1,0),(0,1),(3,0),(0,3),(1,4),(4,1),(4,3),(3,4)
Each of these 8 cells gets probability 0.125.
Total probability on board = 8 * 0.125 = 1.0 (all moves stay on board).
After step 2: redistribute probability from each of those 8 cells to their valid neighbors.
```
* **Pattern Recognition:**
  * Use probability DP when:
    - Computing the probability that a random walk stays within bounds after $K$ steps.
    - Calculating expected game outcomes (e.g. expected number of rolls to finish a board game).
    - Counting paths weighted by probability in stochastic graphs.
* **Core Insight:** Probability mass flows like water. Instead of tracking where each particle goes (forward simulation), we track how much probability mass accumulates at each state after each step. The **Linearity of Expectation** guarantees that we can decompose complex stochastic processes into per-state contributions and sum them. This linearity holds even when the random variables are dependent, making it a uniquely powerful tool.

  Formally: if $P_k(r, c)$ is the probability of being at $(r, c)$ after $k$ steps, then:
  $P_{k+1}(r', c') = \sum_{(r, c) \to (r', c')} P_k(r, c) \cdot p_{transition}$
  
  This is a linear transformation, making the entire process a matrix multiplication under the hood — exactly why Matrix Exponentiation can also solve these if $K$ is enormous.
* **Mistakes Made:** Confusing "probability of still being on the board" with "probability of being at a specific cell." When a knight moves off the board, that probability mass disappears entirely — it doesn't get redistributed. This is modeled naturally by only summing contributions from valid in-bounds cells. A common bug is reflecting out-of-bounds moves back into the board, which changes the problem entirely.
* **What I Learned:** Stochastic processes can be computed exactly through state-space DP. The key insight is to propagate probability as a quantity rather than simulating individual outcomes.

---

## Game Theory (Minimax DP)

* **Problem Type:** Strategic Optimal Play / Minimax DP
* **Data Structure Used:** 2D DP array (indexed by left and right boundaries of a subarray)
* **Approach 1:** Recursive brute force. Generate all possible game trees from every state, explore all moves for both players, and return the optimal outcome. This is $O(2^N)$ time due to exponential branching.
* **Optimized Approach:** Memoized Minimax DP. Define `dp[i][j]` as the maximum score the *current player* (whoever's turn it is) can guarantee if the game is played on the subarray `nums[i..j]`. The current player picks from either end, and the opponent plays optimally on the remaining subarray.
* **Complexity:**
  * **Time:** $O(N^2)$ — there are $O(N^2)$ subproblems, each solved in $O(1)$.
  * **Space:** $O(N^2)$ for the memoization table.
* **Pointer Flow:**
```text
Predict the Winner: nums = [1, 5, 2]
We define dp[i][j] = max score current player can secure from nums[i..j].

Base cases (subarrays of length 1):
dp[0][0] = 1, dp[1][1] = 5, dp[2][2] = 2

Length 2 subarrays:
dp[0][1]: current picks nums[0]=1 -> opponent gets dp[1][1]=5 -> current_gain = 1
          current picks nums[1]=5 -> opponent gets dp[0][0]=1 -> current_gain = 5
          dp[0][1] = max(1, 5) = 5

dp[1][2]: current picks nums[1]=5 -> opponent gets dp[2][2]=2 -> current_gain = 5
          current picks nums[2]=2 -> opponent gets dp[1][1]=5 -> current_gain = 2
          dp[1][2] = max(5, 2) = 5

Length 3 subarray:
dp[0][2]: total = nums[0]+nums[1]+nums[2] = 1+5+2 = 8
          picks nums[0]=1 -> leaves dp[1][2]. Opponent secures dp[1][2]=5.
                          Player 1 total = 1 + (8 - 1 - 5) = 3
          picks nums[2]=2 -> leaves dp[0][1]. Opponent secures dp[0][1]=5.
                          Player 1 total = 2 + (8 - 2 - 5) = 3

Actually, a cleaner formulation:
dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])
This represents: "I pick nums[i] (or nums[j]), and subtract what my opponent secures
                  from the remaining array, because the opponent is equally optimal."

dp[0][2] = max(nums[0] - dp[1][2], nums[2] - dp[0][1])
         = max(1 - 5, 2 - 5)
         = max(-4, -3) = -3

Score difference = -3. Player 1's total = (8 + (-3)) / 2 = 2.5?
Wait, let's use the sum formulation instead:
Player 1 wins if dp[0][n-1] >= 0 where dp is net advantage.
```
* **Pattern Recognition:**
  * Use Minimax DP when:
    - Two players alternately make optimal moves from a finite state.
    - The problem says "both players play optimally" — this is always a signal.
    - Problems involving picking from the ends of arrays, removing stones/coins.
* **Core Insight:** In a zero-sum game, both players' total scores sum to a constant (the sum of all elements). If the current player can secure a score advantage `dp[i][j]` (their score minus opponent's score from the remaining subarray), then their actual score can be recovered. The key transition is: `dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])`. By subtracting `dp[...]` for the opponent, we fold the minimax recursion into a single formula — the opponent's optimal play on the subarray is exactly what `dp[...]` measures for them when it's their turn.

  **P-positions and N-positions:** In pure combinatorial games, every state is either:
  - **P-position (Previous wins):** Current player loses with optimal play. All moves lead to N-positions.
  - **N-position (Next wins):** Current player wins with optimal play. At least one move leads to a P-position.
  Terminal states (no moves) are P-positions. This recursive classification is the foundation of Sprague-Grundy theory.
* **Mistakes Made:** Confusing whose turn it is in the DP state. When `dp[i][j]` measures the current player's advantage (not a fixed player), we must subtract the opponent's dp value rather than adding it. A common bug is writing `dp[i][j] = max(nums[i] + dp[i+1][j], nums[j] + dp[i][j-1])` which incorrectly adds the opponent's future score to the current player's pick.
* **What I Learned:** Minimax collapses into a single DP formulation when we define the state as "advantage of the current player" rather than "score of player 1." The sign flip at each step (subtracting the opponent's future dp) encodes the alternation of turns elegantly.

---

### Master Patterns Learned

#### 1. The Probability Forward-Propagation Frame
* **Applied to:** Knight Probability, Soup Servings, Dice Roll Probability
* **The Strategy:** Initialize probability at the starting state. On each step, create a fresh next-state grid. Distribute each cell's probability mass to all valid reachable next cells, weighted by transition probability. Iterate for exactly K steps.
* **Code Pattern:**
```python
def knight_probability(n, k, row, col):
    moves = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
    dp = [[0.0] * n for _ in range(n)]
    dp[row][col] = 1.0
    for _ in range(k):
        nxt = [[0.0] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                if dp[r][c] == 0:
                    continue
                for dr, dc in moves:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < n:
                        nxt[nr][nc] += dp[r][c] / 8.0
        dp = nxt
    return sum(dp[r][c] for r in range(n) for c in range(n))
```

#### 2. The Zero-Sum Advantage Minimax Frame
* **Applied to:** Predict the Winner, Stone Game, Optimal Strategy for a Game
* **The Strategy:** Define dp[i][j] as the score advantage the current player achieves over the opponent from the subarray [i..j]. Transition: current player picks left (gaining nums[i], opponent plays dp[i+1][j]) or picks right (gaining nums[j], opponent plays dp[i][j-1]).
* **Code Pattern:**
```python
def can_player_one_win(nums):
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = nums[i]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1])
    return dp[0][n-1] >= 0
```
