# Catalan Numbers

Catalan numbers are a sequence of natural numbers that occur in various counting problems, often involving recursively defined structures.

The $n$-th Catalan number $C_n$ is defined by the formula:
$C_n = \frac{1}{n+1} \binom{2n}{n} = \frac{(2n)!}{(n+1)! \cdot n!}$

For $n \ge 0$, the first few Catalan numbers are:
$1, 1, 2, 5, 14, 42, 132...$

## Classic Applications

1.  **Dyck Words:** The number of valid strings of $n$ pairs of parentheses (e.g., for $n=3$, there are 5 strings: `((()))`, `(()())`, `(())()`, `()(())`, `()()()`).
2.  **Binary Search Trees:** The number of structurally unique Binary Search Trees that can be formed with $n$ nodes.
3.  **Polygon Triangulation:** The number of ways to partition a convex polygon with $n+2$ vertices into triangles by drawing non-intersecting diagonals.
