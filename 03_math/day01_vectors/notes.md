# Vectors

## 1. Motivation

### The problem
Real-world entities rarely have a single defining number — they have *multiple simultaneous properties*, and those properties are correlated in ways that matter. A vector is the mathematical object that lets us bundle these properties into one unit while preserving structure: order, relative scale, and the ability to combine entities algebraically (add them, scale them, compare them).

The deeper insight: a vector isn't just "a list of numbers." It's a list of numbers **plus a coordinate system that gives those numbers meaning**. `[3, 4]` means nothing until you know the axes represent, say, (hours studied, mock test score). Change the basis, and the same physical thing gets different numbers. This is why in ML we normalize/standardize features — we're changing the coordinate system so that "distance" and "magnitude" mean something consistent across dimensions.

Examples:
- Person → `[age, height, weight]`
- House → `[area, bedrooms, age]`
- RGB pixel → `[red, green, blue]`
- ML data point → `[feature₁, feature₂, ..., featureₙ]`

---

## 2. Scalar

### Definition
A scalar is a single real number that carries **magnitude only** — no direction, no positional context. It's a complete answer by itself. `7`, `-3.2`, `π` are scalars.

### Examples
- Temperature: `36.6°C`
- Mass: `70 kg`
- Speed (not velocity): `60 km/h`

### Scalar vs quantity
Not every number-with-units is a scalar in the physics/math sense — the distinction is about **transformation behavior**. A scalar stays the same value regardless of the coordinate system or reference frame you're viewing it from (mass doesn't change if you rotate your axes). A vector's *components* change under rotation even though the vector itself (as a geometric object) doesn't. This is the real test: does the number depend on which direction you're facing? If no → scalar. If yes → you're looking at a component of something bigger (a vector).

---

## 3. Vector

### Definition
A vector is an ordered tuple of numbers `[v₁, v₂, ..., vₙ]` that represents a quantity possessing both **magnitude and direction**, defined relative to an origin and a set of basis directions. Formally, it's an element of a vector space — an object that supports addition and scalar multiplication in a way that stays "closed" (vector + vector = vector, scalar × vector = vector).

### Example
v = [3, 4]

### Components
Each component `vᵢ` is the **projection of the vector onto the i-th basis axis** — i.e., "how far to move along axis i to help construct this vector." `v = [3, 4]` means: move 3 units along the x-axis and 4 units along the y-axis. Components are basis-dependent; the vector itself (as an arrow in space) is not.

### Geometric interpretation
`v = [3, 4]` is an arrow starting at the origin `(0,0)` and ending at `(3,4)`. It encodes:
- **Direction** — the angle it makes with the axes (here, `arctan(4/3) ≈ 53.13°`)
- **Magnitude** — its length (here, `5`, via Pythagoras)

Crucially, this arrow is a **free vector** — it's defined by its direction and length only, not by where it's drawn. You can slide it anywhere in the plane without changing what vector it is. This is what separates a vector from a point.

---

## 4. Point vs Vector

### Point
A point is a fixed **location** in space, described by coordinates relative to a chosen origin. It has no independent existence outside that reference frame — it just *is* a position, like `(3, 4)`.

### Vector
A vector is a **displacement or direction+magnitude**, not tied to any specific location. `[3, 4]` describes "move 3 right, 4 up" — it could start anywhere.

### Key distinction
`(3, 4)` as a point answers *"where?"* — it's an address.
`[3, 4]` as a vector answers *"how far, and which way?"* — it's an instruction.

They look identical numerically only because we conventionally draw vectors starting from the origin, which makes the vector's *endpoint* coincide with a point of the same coordinates. But conceptually:
- A point cannot be added to another point meaningfully (what would `(3,4) + (5,1)` even mean spatially? It's not a standard operation).
- A vector *can* be added to another vector (composition of displacements), and a vector *can* be added to a point (translating that point).

This distinction becomes critical in graphics, physics, and ML: positions (points) and directions/gradients (vectors) transform differently under operations like rotation and translation. Translating the coordinate system moves points, but leaves vectors (as pure direction+magnitude) unchanged.

---

## 5. Displacement

Given:
A = (x₁, y₁)
B = (x₂, y₂)

Displacement:
D = B − A = (x₂ − x₁, y₂ − y₁)

### Interpretation
`B − A` is the vector you'd have to **walk along to get from A to B**. It converts a *relationship between two points* into a *free vector* — stripping away the absolute positions and keeping only "how far, and in what direction." This is the fundamental bridge between points (locations) and vectors (directions): subtracting two points always yields a vector, never a point. This is why, in vector-space formalism, point subtraction is well-defined (→ vector) but point addition is not (there's no natural meaning to "adding two locations").

---

## 6. Vector Addition

Given:
a = [a₁, a₂]
b = [b₁, b₂]

a + b = [a₁ + b₁, a₂ + b₂]

### Geometric interpretation
Vector addition is **composition of displacements** — the "tip-to-tail" rule. Place the tail of `b` at the tip of `a`; the resultant vector `a + b` runs from the tail of `a` to the tip of `b`. This is why it works component-wise: each axis's displacement is independent of the others (orthogonal basis directions don't interfere), so you can just sum the "how far along this axis" contributions separately. It's also why addition is commutative — walking `a` then `b` lands you in the same place as walking `b` then `a` (this is literally the parallelogram law).

---

## 7. Vector Subtraction
a − b = [a₁ − b₁, a₂ − b₂]

### Interpretation
`a − b` is defined as `a + (−b)` — adding the reverse of `b`. Geometrically, it's the vector that points **from the tip of b to the tip of a** (when both are drawn from the same origin). This is exactly the same logic as displacement (§5): subtraction always answers "what do I need to add to `b` to get `a`?" — i.e., the gap between them, expressed as a direction+magnitude.

---

## 8. Scalar Multiplication
cv = [c·v1, c·v2]

### Geometric interpretation
Multiplying by scalar `c` **rescales the vector's length by a factor of |c|**, without changing the line it lies on:
- `c > 1` → stretches the vector
- `0 < c < 1` → shrinks it
- `c < 0` → reverses direction *and* rescales
- `c = 0` → collapses it to the zero vector (no direction, no magnitude)

This is why scalars are called scalars — their defining job is to **scale** vectors. Direction is preserved (or exactly flipped); only magnitude changes. This linearity is the foundation of everything downstream: linear combinations, spans, basis vectors, and eventually matrix transformations are all built from "add vectors" + "scale vectors."

---

## 9. Negative Vector
-v = [-v₁, -v₂]

### Geometric interpretation
`-v` is the same magnitude as `v` but pointing in the exact opposite direction — a 180° rotation. It's the special case `c = -1` of scalar multiplication. Its purpose: it's what makes subtraction well-defined as "addition of the opposite" (`a - v = a + (-v)`), and it's why every vector space must contain an additive inverse for closure under addition.

---

## 10. Magnitude

### Geometric motivation
A vector's components describe displacement along each axis independently. Since these axes are orthogonal (perpendicular), the *total straight-line length* of the vector isn't the sum of components — it's the hypotenuse of a right triangle formed by them. This is exactly the setup Pythagoras solved: two legs at right angles, one hypotenuse.

### 2D
For `v = [v₁, v₂]`:
||v|| = √(v₁² + v₂²)

Direct application of the Pythagorean theorem, where `v₁` and `v₂` are the two legs of the right triangle.

### n-dimensional form
||v|| = √(v₁² + v₂² + ... + vₙ²) = √(Σ vᵢ²)

This generalizes because each pair of orthogonal axes contributes independently to squared length — you can prove this by induction, applying Pythagoras repeatedly across dimensions (the diagonal of a box in 3D is the hypotenuse of a triangle whose one leg is itself the 2D diagonal, and so on).

### Interpretation
Magnitude is the **scalar length of the vector** — how "big" the displacement or quantity is, independent of direction. In ML, `||v||` shows up constantly: as a regularization penalty (L2 norm), as the size of a gradient step, and as a building block for distance and normalization.

---

## 11. Unit Vector

### Definition
A unit vector is any vector with magnitude exactly `1`. It carries **pure direction information**, with the "how much" completely factored out.

### Construction
Given any non-zero vector `v`, divide it by its own magnitude:
û = v / ||v||

This works because scalar multiplication rescales length linearly — dividing by `||v||` forces the new magnitude to `||v|| / ||v|| = 1`, while the direction (the ratio between components) is preserved untouched. It's undefined only for the zero vector, since `||0|| = 0` and division by zero has no meaning (the zero vector has no direction to isolate).

---

## 12. Normalization

### Definition
Normalization is the process of rescaling a vector to unit length while preserving its direction — literally the construction in §11 applied as a general operation.

### Formula
v_normalized = v / ||v||

### Why normalization?
Because raw magnitude often encodes *scale artifacts* we don't want influencing a computation. Examples:
- **Cosine similarity** compares only direction (e.g., "are these two documents about similar topics?"), so both vectors are normalized first to remove the effect of document length.
- **ML feature vectors** are normalized so that no single feature dominates a distance/gradient calculation purely because it happens to be measured in bigger units (e.g., "salary in rupees" vs "age in years").
- **Physics/graphics** use unit vectors to represent pure directions (surface normals, light directions) where magnitude would be meaningless or misleading.

---

## 13. Distance

Given:
A = (x₁, y₁)
B = (x₂, y₂)

### Displacement
D = B − A = (x₂ − x₁, y₂ − y₁)

### Distance
d(A, B) = ||B − A|| = √((x₂−x₁)² + (y₂−y₁)²)

Distance is just the *magnitude of the displacement vector* between two points — there's no separate "distance formula" to memorize; it falls directly out of composing two ideas you already have.

### Key relationship
Point difference → displacement vector → magnitude → distance

This chain is the conceptual core of the whole day: distance isn't a primitive concept — it's built from vector subtraction + vector magnitude. Understanding this chain means you never need to memorize the distance formula; you can always re-derive it.

---

## 14. Dimension

### 1D
A single number line. One degree of freedom — one basis direction. `v = [v₁]`.

### 2D
A plane. Two independent directions (e.g., x, y) needed to specify any point/vector uniquely. `v = [v₁, v₂]`.

### 3D
Space as we experience it. Three independent, mutually orthogonal directions. `v = [v₁, v₂, v₃]`.

### nD
Dimension is not fundamentally about "space we can see" — it's about **the number of independent pieces of information (degrees of freedom) needed to fully specify the vector**. Once you decouple "dimension" from "spatial visualization," extending to `n` dimensions is just extending the tuple: `v = [v₁, v₂, ..., vₙ]`, with all the same algebra (addition, scaling, magnitude) applying unchanged.

---

## 15. R², R³ and Rⁿ

### R²
The set of all ordered pairs of real numbers `(x, y)` — the standard 2D plane. Every 2D vector lives here.

### R³
The set of all ordered triples `(x, y, z)` — standard 3D space.

### Rⁿ
The generalized set of all ordered n-tuples of real numbers. `Rⁿ = {(x₁, x₂, ..., xₙ) : xᵢ ∈ R}`. This is the abstract vector space our vectors "live" in once we drop the requirement of physical visualizability. All the operations we defined (addition, scalar multiplication, magnitude, distance) are defined purely algebraically on tuples, so they carry over to `Rⁿ` for any `n` without modification — the geometry is a *consequence* of the algebra, not a prerequisite for it.

---

## 16. High-dimensional vectors

Example:
x = [
area,
bedrooms,
bathrooms,
age,
distance
]

This is a vector in `R⁵`. We cannot draw a 5-axis picture the way we draw arrows in `R²`, but **nothing about "vector-ness" required visualizability in the first place** — it required only that addition and scalar multiplication behave linearly and consistently, and that magnitude/distance be computable via the same sum-of-squares formula. Since those algebraic properties hold identically regardless of `n`, `x` is a perfectly legitimate vector.

This is the conceptual leap that unlocks all of ML: a house, a customer, an image (millions of pixel-intensity dimensions), or a word embedding (hundreds of dimensions) are all just points/vectors in some `Rⁿ`. Distance in that space becomes "how similar are these two things" — the entire basis for nearest-neighbor algorithms, clustering, and much of deep learning's geometric intuition (e.g., embedding spaces).

---

## 17. Vector Operations Summary

| Operation | Meaning | Geometric interpretation |
|---|---|---|
| `a + b` | Component-wise sum | Tip-to-tail composition of displacements |
| `a - b` | Component-wise difference | Vector from tip of `b` to tip of `a` |
| `ca` | Scale each component by `c` | Stretches/shrinks (and flips if `c<0`) the vector along its own line |
| `-a` | Multiply by `-1` | 180° reversal of direction, same magnitude |
| `‖a‖` | `√(Σaᵢ²)` | Straight-line length of the vector (hypotenuse via Pythagoras) |
| `a / ‖a‖` | Normalize | Same direction, forced to unit length (1) |

---

## 18. Important Takeaways

1. **A vector is not "just a list of numbers"** — it's a direction+magnitude defined relative to a basis; the numbers (components) are basis-dependent, but the underlying geometric object is not.
2. **Points and vectors are fundamentally different types** — points are positions; vectors are free-floating displacements. Subtracting two points is the well-defined bridge between them.
3. **Every "new" formula is really a composition of two ideas**: distance = magnitude of displacement; displacement = point subtraction. Once vector addition/subtraction and magnitude are understood, almost everything else can be re-derived rather than memorized.
4. **Magnitude and normalization decompose a vector into "how much" and "which way"** — a separation that's essential for similarity measures, regularization, and physical direction vectors.
5. **Dimension is an algebraic concept, not a visual one.** Once operations are defined purely via component-wise arithmetic, they extend unchanged to any `n`, which is exactly why ML can operate in feature spaces with thousands of dimensions we could never draw.

---

## 19. Questions I should be able to answer

- What is a scalar?
- What is a vector?
- What is the difference between a point and a vector?
- Why can a vector be translated?
- Why does vector addition work component-wise?
- Why does scalar multiplication behave the way it does?
- Where does the magnitude formula come from?
- Why is distance the magnitude of a displacement?
- What does dimension mean?
- Why can vectors exist in thousands of dimensions?
