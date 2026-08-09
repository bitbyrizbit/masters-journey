# Applications

## 1. Data as Vectors

Real-world object
→
numerical representation
→
vector
→
mathematical operations
→
machine learning

### Explanation

Machine learning systems can only operate on numbers — they have no innate understanding of "a house" or "a sentence." So the first step in *any* ML pipeline is translation: take a real-world object and encode its relevant properties as numbers. But scattering those numbers as independent variables would throw away the fact that they belong together and describe *one* entity. Packaging them as a vector preserves that structure while unlocking a toolbox of consistent operations — addition (combine/aggregate), scalar multiplication (weight/scale), magnitude (measure size), and distance (measure similarity). This is why "vectorization" is the near-universal first step in ML: it's not a stylistic choice, it's what makes the rest of the mathematical machinery (linear algebra, calculus, optimization) applicable at all.

---

## 2. Tabular Data

Example:

A house:

- area = `1450`
- bedrooms = `3`
- bathrooms = `2`
- age = `12`
- distance_to_city = `6.5`

Represent it as:


x = [1450, 3, 2, 12, 6.5]


### Why is this useful?

Once the house is a vector in `R⁵`, I can do things that would be meaningless on a spreadsheet row treated as disconnected fields:
- Compute the **distance** between two houses (`‖x₁ − x₂‖`) as a proxy for "how similar are these two listings."
- Feed `x` directly into a **linear model**: `price ≈ w·x + b`, where the model's job reduces to finding the right weight vector `w`.
- **Batch** thousands of houses into a matrix (stack of vectors) and operate on all of them simultaneously using matrix operations, instead of looping through fields one at a time.

The vector form is what makes a house "algebra-compatible."

---

## 3. Images

An RGB pixel can be represented as:


[R, G, B]


Example:


[120, 50, 200]


### What does each component represent?

Each component is the **intensity of one color channel** at that pixel — Red = `120`, Green = `50`, Blue = `200` (on a typical 0–255 scale). Just like a house-vector's components represent independent measurable attributes, a pixel-vector's components represent independent *color channels* that combine to produce the perceived color.

### How could an entire image become numerical data?

An image is a grid of pixels, and each pixel is itself a 3-component vector. Flatten the whole grid (row by row) into one long list, and the entire image becomes a single vector with `height × width × 3` components. A modest `224×224` RGB image, for instance, becomes a vector with over 150,000 dimensions. This is exactly the high-dimensional case from Day 1's core notes — we can't visualize a 150,000-dimensional arrow, but every operation (distance, magnitude, addition) still applies unchanged, which is precisely what lets neural networks treat images as points in a giant vector space and learn geometric structure (similar images cluster together, transformations correspond to movements within that space) without ever needing a picture of the space itself.

---

## 4. Text

Words/documents can eventually be represented numerically.

Examples:

"king" → vector
"queen" → vector
"dog" → vector
"cat" → vector

### Why would representing language as vectors be useful?

Words on their own are symbols with no inherent numerical or geometric structure — you can't add "king" + "queen" or ask how "far" they are from each other. But if each word is mapped to a vector such that **semantic relationships translate to geometric relationships**, suddenly a huge amount of meaning becomes computable: words used in similar contexts end up close together (small distance), and relationships like "royalty" or "gender" can show up as consistent directions in the space (the classic `king − man + woman ≈ queen` illustration). This turns language understanding into a geometry problem — the entire reason vectors are the backbone of NLP.

---

## 5. Embeddings

### What is an embedding?

Based on what I understand today, an embedding is a **learned vector representation of an object (word, image, document, user, etc.) designed so that geometric relationships in the vector space reflect meaningful relationships in the real world** — usually similarity or relatedness. It's different from a "raw" feature vector (like the house example) in that its components aren't hand-picked, interpretable attributes — they're numbers a model has learned specifically to make distance/direction in that space carry semantic meaning.

### Why are vectors useful for embeddings?

Because embeddings are only useful if you can *do something* with them afterward — compare, cluster, search, feed into further models. Vectors are exactly the object that supports all of that: consistent addition, scaling, magnitude, and distance, all of which the embedding is deliberately structured to exploit (e.g., "nearby vectors = similar meaning").

*(Not going deeper into embedding algorithms today — just establishing why the target output has to be a vector in the first place.)*

---

## 6. Similarity

Suppose two objects are represented as vectors.

What might vector distance tell us?

If two vectors are close together (`‖a − b‖` is small), it suggests the two underlying objects are similar *along the dimensions that were encoded* — similar houses, similar images, similar word meanings, depending on context. Distance becomes a proxy for **relatedness**, which is the foundation of nearest-neighbor search, clustering, recommendation systems, and retrieval.

### Important warning

Is Euclidean distance automatically meaningful for every dataset?

No — and this is something I want to stay skeptical about rather than assume. Euclidean distance silently assumes every dimension is on a comparable scale and equally important. If one feature ranges in the thousands (e.g., area in sq ft) and another ranges 0–5 (e.g., bedrooms), the larger-scale feature will dominate the distance calculation regardless of whether it's actually the more *relevant* feature for the task. So Euclidean distance is only meaningful once the vector space has been deliberately constructed (via normalization/standardization, or via a learned embedding) so that closeness in that space actually corresponds to closeness in meaning. It's a *default tool*, not a guarantee — this is a question I want to keep revisiting as I go deeper (cosine similarity, learned distance metrics, etc. are all responses to this exact limitation).

---

## 7. Normalization in ML

Why might removing scale from a representation be useful?

Because scale differences between features can silently bias every downstream computation that depends on magnitude — distance calculations, gradient-based optimization, regularization penalties. If one feature dominates purely due to its units (e.g., "salary in rupees" vs. "years of experience"), models will implicitly treat it as more important, regardless of its actual predictive value. Normalization levels the playing field so that comparisons and learned weights reflect genuine relationships in the data, not artifacts of measurement units.

Potential future connections:

- **feature scaling** — standardizing raw tabular features before training so no feature dominates by scale alone
- **cosine similarity** — comparing pure direction (normalized vectors) instead of magnitude, useful when "how similar" shouldn't depend on "how large"
- **embeddings** — many embedding spaces are explicitly trained/used with normalized vectors so similarity search is scale-independent
- **optimization** — gradient descent converges more reliably when input features are on comparable scales
- **neural networks** — techniques like batch/layer normalization are the same underlying idea applied *inside* the network, not just at the input

---

## 8. High-Dimensional Representation

Why can ML systems work with vectors containing:

100 dimensions?
1,000 dimensions?
10,000 dimensions?

Because every operation ML actually needs — addition, scalar multiplication, dot product, magnitude, distance — is defined purely algebraically as a sum over components (`Σ`), with **no dependency on human visualizability**. A sum over 3 terms and a sum over 10,000 terms follow the exact same rule; only the amount of computation changes, not the underlying mathematics. This is precisely the point established in Day 1's core derivations (§6, §16): dimension is a *count of independent degrees of freedom*, not a spatial constraint. So ML systems don't "struggle" with high dimensions conceptually — the real challenges that show up at high dimensionality (sparsity, the curse of dimensionality, computational cost) are practical/statistical issues layered on top of a mathematical foundation that itself scales without friction.

---

## 9. Connection to Future Topics

### Statistics

Vectors let us represent an entire *dataset* as a cloud of points in space, which is what makes concepts like mean (average vector), variance, and covariance (spread and relationships between dimensions) well-defined and computable — statistics on multivariate data is fundamentally vector geometry in disguise.

### Linear Algebra

Vectors are the atomic objects; linear algebra is the study of how they can be transformed (via matrices), combined (linear combinations, span, basis), and structured (vector spaces, rank, eigenvectors). Today's vector operations (addition, scaling) are literally the two defining axioms of a vector space — everything in linear algebra builds directly on top of them.

### Machine Learning

Nearly every ML model — from linear regression to deep networks — is, at its core, a function that consumes vectors and produces vectors (or scalars). Feature vectors in, prediction vectors out; the model itself is usually a sequence of vector transformations (matrix multiplications) with some nonlinearity in between.

### Deep Learning

Every layer of a neural network takes an input vector, applies a linear transformation (matrix multiply — a generalized combination of the addition/scaling operations from today) plus a nonlinearity, and produces a new vector. Every intermediate representation inside a network — hidden activations, attention scores, gradients — is a vector living in some learned space.

### Embeddings

Embeddings are the clearest real-world payoff of everything covered today: they take non-numeric objects (words, images, users) and place them into a vector space specifically engineered so that distance and direction encode meaning — turning "understanding relationships between things" into "doing geometry," which is exactly the shift these notes have been building toward all day.
