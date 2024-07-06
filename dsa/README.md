# Introduction

This contains Data Structures and Algorithms practice material.

# Links

Overview:
https://www.geeksforgeeks.org/learn-data-structures-and-algorithms-dsa-tutorial/?ref=lbp

* Heaps:
    - https://www.youtube.com/watch?v=pAU21g-jBiE&ab_channel=MichaelSambol
    - https://stackoverflow.com/questions/9755721/how-can-building-a-heap-be-on-time-complexity
    - https://leetcode.com/problems/k-closest-points-to-origin/
* Longest increasing subsequence:
    - https://en.wikipedia.org/wiki/Longest_increasing_subsequence
* Bellman Ford:
    - https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm 
    - shortest path faster algorithm: https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm#Improvements
        - TODO: would be interesting to compare its run time with optimized implementations of alternatives like Dijkstra's algorithm, bellman ford, etc.
        - TODO: implement negative cycle detection using this
* Johnson's algorithm:
    - https://en.wikipedia.org/wiki/Johnson%27s_algorithm
    - TODO: understand this
* Kosaraju SCC;
    - reverse edges and descing sort by finish time
    - do succsssive rounds of DFS in descending order of finish times to identify SCCs
    - Note: reversing edges in stage-1 is necessary because nodes with highest finish times only have useful properties. Nodes with lowest finish times can be anywhere in the graph and have no useful properties.
* TODO: understand Tarjan SCC
* TODO: KMP
* Catalan Numbers:
    - analytical formula proof: https://en.wikipedia.org/wiki/Catalan_number#Second_proof
    - list of things that are catalan numbers: https://www.geeksforgeeks.org/applications-of-catalan-numbers/
* TODO: understand modular inverse, fermats theorem, group theory, and related concepts
* Euler product formula:
    - intuition: https://en.wikipedia.org/wiki/Euler%27s_totient_function#Computing_Euler's_totient_function
* TODO: chinese remainder theorem
* convex hull:
    - https://cp-algorithms.com/geometry/convex-hull.html
* closest pair of points
    - https://cp-algorithms.com/geometry/nearest_points.html
* TODO: skip list
* TODO: maxflow-mincut, fft, sparse table, segment trees
