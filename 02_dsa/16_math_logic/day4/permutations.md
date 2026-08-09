# Permutations

A permutation is an arrangement of all or part of a set of objects, where the **order of arrangement matters**.

## 1. Permutations of $N$ Distinct Objects
The number of ways to arrange $n$ distinct objects in a line is:
$P(n) = n! = n \cdot (n-1) \cdot ... \cdot 1$

## 2. Permutations of $R$ Objects from $N$ Distinct Objects
If we want to select and arrange $r$ objects out of $n$ distinct objects:
$P(n, r) = \frac{n!}{(n-r)!}$

## 3. Permutations with Repetition (Duplicate Objects)
If we have a set of $n$ objects where $n_1$ are of type 1, $n_2$ are of type 2, etc.:
$P = \frac{n!}{n_1! \cdot n_2! \cdot ... \cdot n_k!}$
*Example:* Arranging the letters in the word "BALLOON" ($n=7$, L appears 2 times, O appears 2 times) yields $\frac{7!}{2! \cdot 2!} = 1260$ arrangements.
