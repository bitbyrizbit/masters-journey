# Exercises

## Part A — Calculation

### Exercise 1


a = (2,3)
b = (4,-1)


Find:

1. a + b
2. a - b
3. 3a
4. -2b

### Answer

1. `a + b = (2+4, 3+(-1)) = (6, 2)`
2. `a - b = (2-4, 3-(-1)) = (-2, 4)`
3. `3a = (3·2, 3·3) = (6, 9)`
4. `-2b = (-2·4, -2·(-1)) = (-8, 2)`

---

## Exercise 2

Find the magnitude:


v = (6,8)


### Answer


‖v‖ = √(6² + 8²) = √(36+64) = √100 = 10

The components form a right triangle with legs 6 and 8; the vector is the hypotenuse — length 10.

---

## Exercise 3

Normalize:


v = (6,8)


Then verify manually that the resulting vector has magnitude 1.

### Answer

`‖v‖ = 10` (from Exercise 2).


û = v / ‖v‖ = (6/10, 8/10) = (0.6, 0.8)


Verify:

‖û‖ = √(0.6² + 0.8²) = √(0.36 + 0.64) = √1 = 1 ✓


---

## Exercise 4

Find the distance between:


A = (2,3)
B = (8,11)


### Answer

Displacement: `D = B - A = (8-2, 11-3) = (6, 8)`

Distance = magnitude of displacement:

d(A,B) = √(6² + 8²) = √(36+64) = √100 = 10


---

## Exercise 5

Given:


a = (1,2,3)
b = (4,5,6)


Find:

1. a + b
2. ||a||

### Answer

1. `a + b = (1+4, 2+5, 3+6) = (5, 7, 9)`
2. `‖a‖ = √(1² + 2² + 3²) = √(1+4+9) = √14 ≈ 3.742`

---

# Part B — Conceptual

## Q1

Why can a vector be moved around without changing the vector itself?

### Answer

A vector is defined purely by its magnitude and direction — never by an absolute position. Its components are computed as `Q - P` (endpoint minus start point), and when you translate both endpoints by the same offset, that offset cancels out in the subtraction (`(Q+t) - (P+t) = Q - P`). So sliding the vector anywhere in space leaves its components — and therefore its identity — completely unchanged.

---

## Q2

Why are a point and a vector not conceptually the same thing even though both can be represented using coordinates?

### Answer

A point answers "where is it?" — it's a fixed address that only makes sense relative to a chosen origin, and it cannot be translated without becoming a *different* point. A vector answers "how far, and which way?" — it's a portable instruction that stays the same vector no matter where you draw it. They can share identical numbers only because we conventionally draw a vector's tail at the origin, making its tip coincide with the point of the same coordinates — but that's a drawing convention, not evidence they're the same kind of object.

---

## Q3

Why does multiplying a vector by 2 change its magnitude but not its direction?

### Answer

`2v` is `v + v` — walking along `v`, then walking along `v` again from where you landed. Since both walks point the same way, the tip-to-tail construction just continues in a straight line, doubling the length without introducing any new direction. Scalar multiplication by a positive number only rescales "how many copies" of the same directional step you're taking.

---

## Q4

Why does multiplying a vector by -1 reverse its direction?

### Answer

`-v` is defined as the vector that satisfies `v + (-v) = 0` — the exact "undo" of `v`. The only way walking `v` and then `-v` can bring you back to the start is if `-v` has the same length as `v` but points 180° opposite. So the sign flip on every component isn't arbitrary — it's forced by the requirement that vectors have additive inverses.

---

## Q5

Why does normalization preserve direction?

### Answer

Normalization divides every component by the same scalar (`‖v‖`). Direction is determined by the *ratios* between components (e.g., "twice as much x-displacement as y-displacement"). Dividing all components by an identical number preserves every one of those ratios exactly, so the angle the vector makes with the axes never changes — only the overall scale shrinks, down to exactly magnitude 1.

---

## Q6

Why is distance between two points equal to the magnitude of their difference?

Do not answer with "because that's the formula."

### Answer

Distance is meant to capture "the length of the straight path connecting two points." Subtracting two points (`B - A`) produces exactly the displacement vector describing that straight path — direction and size of the gap between them. Magnitude then strips away the direction and keeps only the size. So distance was never an independent concept — it's the direct consequence of first finding the connecting vector, then measuring its length.

---

## Q7

Why can a vector have 1,000 dimensions even though we cannot visualize it?

### Answer

A vector is fundamentally an algebraic object — a tuple with defined component-wise addition and scalar multiplication — not a picture. Every operation we rely on (addition, scaling, magnitude via `√Σvᵢ²`, distance) is defined as arithmetic over components, and none of that arithmetic requires the result to be drawable. Our inability to visualize 1,000 dimensions is a limitation of human perception, not a limitation of the mathematics — the same sum-of-squares rule that works for 2 terms works identically for 1,000.

---

# Part C — Thought Experiment

## Q8

Person A:


height = 180
weight = 75


Person B:


height = 180
weight = 75


Represent both as vectors.

What is their Euclidean distance?

### Answer


A = [180, 75]
B = [180, 75]

d(A,B) = √((180-180)² + (75-75)²) = √0 = 0


Zero distance — the two vectors are identical, which makes sense: A and B have exactly the same measured attributes, so nothing distinguishes them in this feature space.

---

## Q9

Person C:


height = 181
weight = 75


Compare C with A.

### Answer


A = [180, 75]
C = [181, 75]

d(A,C) = √((181-180)² + (75-75)²) = √(1+0) = 1


A small distance of 1, reflecting a 1 cm height difference with everything else identical. Note how "small" this distance is *only because* height happens to be measured in centimeters here — if height were measured in meters instead (`1.80` vs `1.81`), the same real-world difference would produce a distance of `0.01`, showing that the raw numeric distance is sensitive to units, not just to "how different" the two people actually are.

---

## Q10

Is Euclidean distance automatically a meaningful measure of similarity for every dataset?

### Answer

No. As Q9 shows, Euclidean distance is entirely dependent on the *units and scale* chosen for each feature — a feature with a larger numeric range will dominate the distance calculation regardless of whether it's actually more meaningful for judging similarity. For distance to be a fair measure of similarity, every dimension needs to be on a comparable scale (via normalization/standardization), and even then, straight-line distance assumes a kind of uniform, isotropic relationship between dimensions that may not match how "similarity" actually behaves for the data in question. Euclidean distance is a reasonable *default*, not a guaranteed-correct measure — its meaningfulness has to be earned by how the feature space was constructed.

---

# Part D — Reconstruction Challenges

## Q11

Suppose you forget the vector magnitude formula.

Starting only from geometry and Pythagoras, reconstruct it.

### Answer

Draw `v = [v₁, v₂]` as an arrow from the origin to `(v₁, v₂)`. Drop a vertical line from `(v₁,v₂)` down to `(v₁, 0)`. This creates a right triangle: horizontal leg `v₁`, vertical leg `v₂`, and the vector itself as the hypotenuse (the two legs meet at 90° since the axes are perpendicular). By Pythagoras, `hypotenuse² = v₁² + v₂²`, so `‖v‖ = √(v₁² + v₂²)`. For higher dimensions, treat each additional axis as perpendicular to everything accumulated so far, and reapply Pythagoras recursively — giving `‖v‖ = √(v₁² + v₂² + ... + vₙ²)` in general.

---

## Q12

Explain why vector addition is component-wise without quoting the rule first.

### Answer

Adding two vectors means walking along one, then continuing along the other from wherever you land (tip-to-tail). Since the x-axis and y-axis are independent (motion along one has zero effect on position along the other), the total horizontal displacement after both walks is just the sum of each walk's horizontal part, and likewise for vertical. There's no interaction between axes to account for, so each component can be summed on its own — which is exactly what "component-wise addition" means.

---

## Q13

Explain why normalization removes scale while preserving direction.

### Answer

Direction is encoded in the *relative proportions* between a vector's components, not their absolute size. Dividing every component by the same number (the vector's own magnitude) scales all of them down by an identical factor, so every ratio between components is preserved exactly — meaning the direction is untouched. What does change is the overall size, which shrinks precisely to 1 because dividing a quantity by itself always yields 1. In effect, normalization surgically removes "how big" while leaving "which way" completely intact.

---

# Part E — Self-Test

Without notes, explain:

1. Scalar
2. Vector
3. Point
4. Displacement
5. Vector addition
6. Scalar multiplication
7. Magnitude
8. Unit vector
9. Normalization
10. Distance
11. Dimension
12. R² / R³ / Rⁿ
13. Why vectors are useful in ML

### My answers

1. **Scalar** — a single real number carrying magnitude only, with no direction; its value doesn't depend on the coordinate system or orientation you view it from.
2. **Vector** — an ordered tuple of numbers representing magnitude *and* direction relative to a basis; defined by consistent rules for addition and scalar multiplication, and free to be translated without changing identity.
3. **Point** — a fixed location in space relative to an origin; unlike a vector, it can't be meaningfully translated without becoming a different point.
4. **Displacement** — the vector `B - A` connecting two points; it converts a relationship between two fixed locations into a portable direction+magnitude.
5. **Vector addition** — tip-to-tail composition of two displacements, computed component-wise because independent (orthogonal) axes never interfere with each other.
6. **Scalar multiplication** — rescaling a vector's length by a factor `c` (and flipping direction if `c<0`) while keeping it on the same line, since it's equivalent to repeatedly adding the vector to itself.
7. **Magnitude** — the straight-line length of a vector, derived by treating its components as legs of a right triangle and applying Pythagoras (`√Σvᵢ²`), generalized recursively across dimensions.
8. **Unit vector** — any vector with magnitude exactly 1; represents pure direction with the "how much" completely factored out.
9. **Normalization** — dividing a vector by its own magnitude to produce a unit vector in the same direction, since dividing every component by the same scalar preserves all their ratios (direction) while collapsing length to 1.
10. **Distance** — the magnitude of the displacement vector between two points; not an independent formula, but a direct consequence of "subtract to get displacement, then measure its length."
11. **Dimension** — the number of independent degrees of freedom (components) needed to fully specify a vector; a purely algebraic property, not inherently tied to visualizability.
12. **R² / R³ / Rⁿ** — the sets of all ordered pairs / triples / n-tuples of real numbers; the abstract spaces vectors "live in," where all operations are defined algebraically and apply identically regardless of how large `n` is.
13. **Why vectors are useful in ML** — real-world objects have multiple attributes that need to be treated as one unit; representing them as vectors gives access to a consistent algebra (addition, scaling, distance, linear transformations) that underlies virtually every ML operation, from feature engineering to neural network layers to embedding similarity.