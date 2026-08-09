# Derivations

## 1. Vector Addition

Given:
a = [2, 1]
b = [3, 2]

### Geometric reasoning

To add two vectors, I place them tip-to-tail: draw `a` starting from the origin, ending at `(2,1)`. Then draw `b` starting from *there* — i.e., from `(2,1)` — instead of from the origin. Since `b = [3,2]` means "move 3 right, 2 up" *regardless of starting point* (translation invariance, see §9), walking it from `(2,1)` lands me at `(2+3, 1+2) = (5,3)`. The resultant vector `a+b` is the single arrow from the original origin straight to this final point `(5,3)` — it represents the *net* displacement of doing both walks in sequence.

### Component-wise result
a + b = [2+3, 1+2] = [5, 3]

### General form
a = [a₁, a₂]
b = [b₁, b₂]

a + b = [a₁ + b₁, a₂ + b₂]

### Why this is not an arbitrary rule

It falls directly out of the tip-to-tail geometric construction — it isn't a rule invented for convenience. Because the x-axis and y-axis are orthogonal, motion along one axis has zero effect on position along the other. So the "how far right" contributions from `a` and `b` can be summed completely independently of the "how far up" contributions. If the axes were *not* independent (imagine a skewed, non-orthogonal coordinate system), naive component-wise addition would still work algebraically (vector spaces don't require orthogonality) — but the *clean geometric picture* of "just add the x's and add the y's" is a direct consequence of using an orthonormal basis, which is why it feels so natural in standard Cartesian coordinates.

---

## 2. Vector Subtraction

Given:
a = [5, 4]
b = [2, 1]

### Geometric interpretation

`a − b` is defined as `a + (−b)`. Geometrically, if I draw both `a` and `b` from the same origin, `a − b` is the vector that starts at the tip of `b` and ends at the tip of `a`. Intuition: it answers "what displacement do I need to add to `b` to arrive at `a`?" — which is exactly the gap between their endpoints.

### Component-wise form

a − b = [a₁ − b₁, a₂ − b₂] = [5−2, 4−1] = [3, 3]

This follows immediately from combining addition (§1) with negation (§4): subtracting is adding the negated vector, and negation flips each component's sign, so the components simply subtract term-by-term.

---

## 3. Scalar Multiplication

Given:
v = [2, 3]

Consider `2v`.

### Geometric reasoning

`2v` should mean: walk along `v`, then walk along `v` again, tip-to-tail with itself. By the addition logic in §1, that gives a straight-line path twice as long as `v`, in the exact same direction (since I'm adding a vector to a copy of itself — no new direction is introduced, the tip-to-tail construction just continues along the same line).

### Algebraic result
2v = v + v = [2+2, 3+3] = [4, 6]

Which matches applying the scalar to each component directly: `2·[2,3] = [2·2, 2·3] = [4,6]`.

### General form
v = [v₁, v₂]
cv = [c·v₁, c·v₂]

This generalizes because "c copies of v laid end to end" (for integer c) always sums component-wise by §1's logic, and extending to non-integer/negative c is done by defining scalar multiplication to preserve this same proportional relationship — i.e., we *define* it this way precisely so the geometric picture (stretch/shrink along the same line) stays consistent for all real c.

---

## 4. Negative Scalar

Given:
v = [2, 3]

Consider `-v`.

### What should happen geometrically?

`-v` must be the vector that, when added to `v`, gives the zero vector — the "undo" of `v`. The only geometric object satisfying `v + (-v) = 0` is a vector of the *same length* pointing in the *exact opposite direction* (a 180° flip), because that's the only way the tip-to-tail walk of `v` then `-v` returns you exactly to where you started.

### Algebraic result
-v = -1 · v = [-1·2, -1·3] = [-2, -3]

Check: `v + (-v) = [2+(-2), 3+(-3)] = [0,0]` ✓ — confirms the geometric requirement algebraically.

---

## 5. Magnitude in 2D

Given:
v = [3, 4]

### Step 1 — Draw geometry

Draw `v` as an arrow from `(0,0)` to `(3,4)`. Drop a vertical line down from `(3,4)` to `(3,0)`, and a horizontal line along the x-axis from `(0,0)` to `(3,0)`.

### Step 2 — Identify right triangle

These three segments form a triangle:
- horizontal leg, length `3` (the x-component)
- vertical leg, length `4` (the y-component)
- the vector `v` itself, connecting `(0,0)` to `(3,4)` directly, as the hypotenuse

The horizontal and vertical legs meet at `(3,0)` at a **90° angle**, since the x-axis and y-axis are perpendicular by construction. This makes it a right triangle.

### Step 3 — Apply Pythagoras

For a right triangle with legs `p`, `q` and hypotenuse `h`:
h² = p² + q²

Substituting `p = 3`, `q = 4`:

h² = 3² + 4² = 9 + 16 = 25


### Step 4 — Obtain magnitude
h = √25 = 5
⟹ ‖v‖ = 5

So the length of `v = [3,4]` is `5` — not because of a memorized formula, but because the components literally *are* the legs of a right triangle whose hypotenuse is the vector.

---

## 6. Generalizing Magnitude

Start from:

**2D:**
‖[v₁,v₂]‖ = √(v₁² + v₂²)

(directly from §5, general components instead of 3,4)

**3D:**
Think of `v = [v₁, v₂, v₃]` as first moving in the xy-plane to reach `(v₁, v₂, 0)` — that partial displacement has length `√(v₁²+v₂²)` (2D case). Then move vertically by `v₃` to reach the true endpoint. This vertical move is perpendicular to the entire xy-plane, so it forms a *new* right triangle: one leg is the xy-diagonal `√(v₁²+v₂²)`, the other leg is `v₃`, and the hypotenuse is the full 3D vector length.
‖v‖² = (√(v₁²+v₂²))² + v₃² = v₁² + v₂² + v₃²
⟹ ‖v‖ = √(v₁² + v₂² + v₃²)


**nD (generalize):**
‖v‖ = √(v₁² + v₂² + ... + vₙ²) = √(Σᵢ vᵢ²)


### Why does the same idea continue working?

Each new dimension can be treated as "one more perpendicular step" on top of everything already accumulated in the lower dimensions. Because that new axis is, by definition, orthogonal to all the previous ones combined, the "already-accumulated diagonal" and the "new leg" always form a fresh right triangle — so Pythagoras applies again, recursively, no matter how many dimensions you add. The magnitude formula isn't a separate rule per dimension; it's the *same* right-triangle argument applied repeatedly.

---

## 7. Unit Vector / Normalization

Given:
v = [3, 4]

### Step 1

Find magnitude.
‖v‖ = √(3² + 4²) = √25 = 5

### Step 2

We want a vector of magnitude 1, pointing the *same direction* as `v`. From §3, scalar multiplication by `c` scales magnitude by `|c|` while preserving direction (for `c>0`). So I need a `c` such that:
c · ‖v‖ = 1  ⟹  c = 1/‖v‖

### Step 3

Construct it.
û = v / ‖v‖ = [3/5, 4/5] = [0.6, 0.8]

### Step 4

Verify its magnitude.
‖û‖ = √(0.6² + 0.8²) = √(0.36 + 0.64) = √1 = 1

### General result
û = v / ‖v‖ = [v₁/‖v‖, v₂/‖v‖, ..., vₙ/‖v‖]

Valid for any non-zero `v`, since dividing by `‖v‖` (a positive scalar) exactly cancels out the vector's own length, leaving a result of magnitude 1 while every component ratio — and thus the direction — is left untouched.

---

## 8. Distance Between Two Points

Given:
A = (1, 2)
B = (5, 5)

### Step 1 — Find displacement
D = B − A = (5−1, 5−2) = (4, 3)

### Step 2 — Interpret displacement geometrically

`D = [4,3]` is the vector describing exactly how to walk from `A` to `B`: 4 units right, 3 units up. It's a free vector — its length and direction encode everything about the "gap" between the two points, independent of where in the plane `A` and `B` actually sit.

### Step 3 — Find magnitude

Using §5's method: this displacement forms a right triangle with legs `4` and `3`.
‖D‖ = √(4² + 3²) = √(16+9) = √25 = 5

### Step 4 — Connect to distance

The straight-line distance between `A` and `B` is, by definition, the length of the shortest path connecting them — which is exactly the length of the displacement vector between them.
d(A,B) = ‖D‖ = 5

### General derivation

For:
A = (x₁, y₁)
B = (x₂, y₂)

1. Displacement: `D = B − A = (x₂−x₁, y₂−y₁)`
2. This displacement's components are the legs of a right triangle (§5's argument, general symbols instead of numbers)
3. Magnitude of that displacement, by Pythagoras:
d(A,B) = ‖D‖ = √((x₂−x₁)² + (y₂−y₁)²)

No formula was memorized — this is just "subtract to get displacement" (§2) chained with "take magnitude" (§5/§6).

---

## 9. Translation Invariance

Show why moving a vector from:

`(0,0) → (3,4)`

to:

`(10,20) → (13,24)`

does not change its components.

### Derivation

A vector drawn from point `P` to point `Q` has components defined as `Q − P` (this is just displacement, §2/§8).

**Case 1:**
P = (0,0), Q = (3,4)
components = Q − P = (3−0, 4−0) = (3,4)

**Case 2:**
P = (10,20), Q = (13,24)
components = Q − P = (13−10, 24−20) = (3,4)

Both cases yield the identical component vector `[3,4]`. This isn't a coincidence — it's structurally guaranteed: adding the same offset `(10,20)` to *both* the start and end point cancels out completely in the subtraction:
Q' − P' = (Q + t) − (P + t) = Q − P + (t − t) = Q − P

where `t = (10,20)` is the translation applied to both points. Since the translation term always cancels, a vector's components depend only on the *relative* offset between its two endpoints — never on their absolute position. This is precisely why vectors are "free" objects that can be moved anywhere without changing what they are.

---

## 10. Optional Reconstruction Challenge

Hide the magnitude formula.

Starting only from:

- coordinates
- geometry
- Pythagoras

reconstruct the magnitude of:
v = [v₁, v₂]

### My derivation

Draw `v` from the origin to `(v₁, v₂)`. Drop a perpendicular from `(v₁,v₂)` to the x-axis at `(v₁, 0)`. This creates a right triangle with:
- horizontal leg = `v₁` (distance from `(0,0)` to `(v₁,0)`)
- vertical leg = `v₂` (distance from `(v₁,0)` to `(v₁,v₂)`)
- hypotenuse = `v` itself

By Pythagoras: `hypotenuse² = v₁² + v₂²`, so:
‖v‖ = √(v₁² + v₂²)

**Extending to n dimensions:** treat the first `n−1` components as already "resolved" into a single diagonal of length `√(v₁² + ... + vₙ₋₁²)` (by induction — assume this holds for `n−1` dimensions). The `n`-th component `vₙ` is measured along an axis perpendicular to all previous `n−1` axes. So the existing `(n−1)`-dimensional diagonal and the new leg `vₙ` again form a right triangle, and Pythagoras applies once more:
‖v‖² = (√(v₁²+...+vₙ₋₁²))² + vₙ² = v₁² + v₂² + ... + vₙ²
⟹ ‖v‖ = √(Σᵢ vᵢ²)

The base case (`n=1`) is trivial: `‖[v₁]‖ = |v₁| = √(v₁²)`. Combined with the inductive step above, this proves the formula for all `n` — magnitude in any dimension is nothing more than Pythagoras applied recursively, one new orthogonal axis at a time.