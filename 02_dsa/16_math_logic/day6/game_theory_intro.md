# Introduction to Game Theory (Minimax)

Game Theory is the study of mathematical models of strategic interaction among rational decision-makers. In coding, this is usually simplified to **Impartial Games** played by two players under perfect information (e.g. Nim, Coin Change Game, Tic-Tac-Toe).

## 1. The Minimax Algorithm
For zero-sum, turn-based games, we assume both players play optimally:
*   **Maximizer (Player 1):** Tries to maximize their score.
*   **Minimizer (Player 2):** Tries to minimize Player 1's score.

At each step, a player chooses the move that leads to the best possible outcome for themselves, assuming the opponent will do the same on their turn.

## 2. Game States (P-positions and N-positions)
For games where you win by making the last move:
*   **P-position (Previous player wins):** The player who just moved is guaranteed to win if they play optimally. (Also called a losing state for the current player).
*   **N-position (Next player wins):** The player whose turn it is now is guaranteed to win if they play optimally. (A winning state for the current player).

### The Rules of Impartial Games
1.  All terminal positions are P-positions (losing states, as no moves remain).
2.  If you can transition to at least one P-position, the current state is an N-position (you make the move to the losing state, forcing your opponent into a loss).
3.  If all possible transitions lead to N-positions, the current state is a P-position (no matter what you do, your opponent is placed into a winning position).
