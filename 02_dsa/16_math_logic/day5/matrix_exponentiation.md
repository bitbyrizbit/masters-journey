# Matrix Exponentiation

Matrix Exponentiation is a technique to solve linear recurrence relations (like the Fibonacci sequence) in logarithmic $O(\log N)$ time instead of linear $O(N)$ time.

## The Linear Transformation

A recurrence relation like $F_n = F_{n-1} + F_{n-2}$ can be framed as a matrix multiplication:
\[
\begin{pmatrix} F_n \\ F_{n-1} \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} F_{n-1} \\ F_{n-2} \end{pmatrix}
\]

By induction:
\[
\begin{pmatrix} F_n \\ F_{n-1} \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^{n-1} \begin{pmatrix} F_1 \\ F_0 \end{pmatrix}
\]

## The Algorithm

To compute the matrix power $T^{n-1}$ in $O(\log n)$ time, we use the **Binary Exponentiation** algorithm (Fast Power) from Day 3, but applied to matrices instead of scalars. 

The multiplication steps involve matrix-matrix multiplication instead of standard multiplication, which takes $O(K^3)$ where $K$ is the size of the transition matrix. For Fibonacci, $K=2$, so matrix multiplication is extremely cheap ($O(8)$ operations).
