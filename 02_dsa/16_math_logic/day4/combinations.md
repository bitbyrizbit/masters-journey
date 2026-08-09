# Combinations

A combination is a selection of items from a collection, such that the **order of selection does not matter**.

## 1. Selecting $R$ Objects from $N$ Distinct Objects
The number of ways to choose $r$ objects out of $n$ distinct objects is denoted by $\binom{n}{r}$ or $C(n, r)$:
$C(n, r) = \frac{n!}{r! \cdot (n-r)!}$

## 2. Pascal's Identity (Combinations DP Relation)
Combinations can be computed dynamically without calculating factorials directly, preventing overflow:
$C(n, r) = C(n-1, r-1) + C(n-1, r)$

This identity is what forms Pascal's Triangle.

## 3. Combinations with Repetition
If we are choosing $r$ objects from $n$ types of objects, where we can choose the same type multiple times (e.g., picking 5 candies from 3 flavor bowls):
$C_{\text{rep}}(n, r) = C(n + r - 1, r) = \frac{(n + r - 1)!}{r! \cdot (n-1)!}$
