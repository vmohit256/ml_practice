
# Notes

- PCA
    - SVD on covariance matrix
        - works best with ellipsoid shaped that comes from y = M*(x+error) where error is gaussian noise. So y_observed - y can be modelled well with multivariate gaussian distribution
        - aligns the ellipsoid and returns standard basis vectors in decreasing order of variance
    - should standardize the data or else the features with larger scale will dominate the variance
- Isomap
- Linear Discriminant analysis ([Reference](https://www.sjsu.edu/faculty/guangliang.chen/Math253S20/lec11lda.pdf))
    - maximize the distance between classes and minimize the variance within classes
    - 2-class variant
        - C1 has {x1, x2, x3, ...} and C2 has {y1, y2, y3, ...}
        - "v" is seperating hyperplane
        - m1 = mean(C1), m2 = mean(C2)
        - mu1 = m1.v, mu2 = m2.v
        - ||mu1 - mu2||^2 = ((m1-m2)^T v)^T (m1-m2)^T v = v^T (m1-m2) (m1-m2)^T v = v^T Sb v
            - Sb is symmetric positive semidefinite with rank 1 and only one positive eigenvalue with eigenvector (m1-m2) unit vector and eigenvalue = ||m1-m2||^2. Coloumn and row space are same
        - variance within classes proportioal to
            - s1^2 = sum_i ((xi - m1). v)^2 = sum_i ((xi - m1)^T v)^T (xi - m1)^T v = sum_i v^T Si1 v = v^T S1 v
                - S1 = sum_i (xi - m1) (xi - m1)^T   // sum of |C1| rank 1 positive semi definite matrices
            - total within class variance = s1^2 + s2^2 = v^T Sw v
                - Sw = S1 + S2
        - objective function: v* = argmax_v (v^T Sb v) / (v^T Sw v)
            - assume Sw is invertible. If not, then the objective function blows up to infinity
            - write Sw = R^T R where R is full rank using eigenvalue decomposition
            - v* = argmax_v (v^T Sb v) / (v^T R^T R v)
            - define u = R v, so v = R^-1 u
            - u* = argmax_u ((R^-1 u) . (m1-m2))^2 / (u.u)
            - TODO: continue this line of reasoning to get a intuitive understanding of LDA
                - this is maximized by picking u such that R^-1 u is in the direction of m1-m2



# References

