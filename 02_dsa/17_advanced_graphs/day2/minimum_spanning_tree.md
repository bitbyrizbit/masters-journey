# Minimum Spanning Tree (MST)

A Minimum Spanning Tree (MST) is a subset of the edges of a connected, edge-weighted undirected graph that connects all the vertices together, without any cycles, and with the minimum possible total edge weight.

For any graph with $V$ vertices, its spanning tree must have exactly $V-1$ edges.

## Two Classic Algorithms

1.  **Kruskal's Algorithm:**
    *   An edge-centric greedy algorithm.
    *   Sorts all edges by weight, and adds them one by one to the tree unless the edge forms a cycle.
    *   Utilizes DSU to check and prevent cycle formation.
    *   Runs in $O(E \log E)$ or $O(E \log V)$ time.
2.  **Prim's Algorithm:**
    *   A vertex-centric greedy algorithm.
    *   Builds the tree node by node. Starts at an arbitrary root vertex, and repeatedly adds the shortest edge connecting a vertex in the tree to a vertex outside the tree.
    *   Utilizes a min-heap to quickly locate the shortest connecting edge.
    *   Runs in $O(E \log V)$ time.
