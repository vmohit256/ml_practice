# Types of Models

1. Decision Trees
    - Classification, Regression
    - const functions: gini impurity, entropy, mse
    - CART algorithm
        - greedy (optimization problem is NP complete)
        - pick (feature, split) that minimizes cost
    - Pros: explainable, efficient to infer (O(logn))
    - methods of regularization (reduce variance and increase bias)
        - min_samples_split, min_samples_leaf, min_weight_fraction_leaf, min_samples_leaf -> increase
        - max_leaf_nodes, max_features -> decrease
        - other algorithms first grow tree without restrictions and then prune it
    - Cons:
        - non-parametric, high variance, easy to overfit
        - source of bias: vertical / horizontal decision boundaries -> rotation messes up predictions -> pca may solve it??
        - instability, produces wildly different model in each run
    - feature importance
        - importance features are closer to root
2. Hard Voting
    - aggregate all kinds of models (SVM, Decision trees, etc.) and pick most frequent output label
    - intuition: biased coin with only 0.51 probability of heads will give 0.75 probability of heads if spun 1000 times
    - models should make different kinds of independent errors (eg: very different architectures)
3. Bagging (Booststrap Aggregating)
    - create N subsets of training data by sampling (with replacement) independently (called bootstrapping)
    - Pasting: same as bagging but sampled with replacement
        - bagging often works better (TODO: didn't really understand the logic of the book)
    - learn classifiers separately on each subset and aggregate by hard voting (call aggregating)
    - highly parallelizable and very easy to scale
    - reduces variance (without affecting bias!) at the cost of more computational resources
    - Out-of-bag evaluation
        - each weak learner has >= 37% of original training data absent in its training data
            - evaluate weak learner on out of bag samples -> no need for cross validation!
            - evaluate ensemble by aggregating only oob predictions and checking accuracy on train
    - sampling features for weak learners
        - very useful for high-dimensional data
4. Random Forests
    - Decision Trees + Bagging 
    - pick best features only on randomly selected subset -> greater tree diversity -> higher bias and lower variance per weak learner
    - Extra-Trees (Extremely Randomized Trees)
        - use random thresholds instead of optimized ones
        - increase bias nad reduce variance even more per weak learner
        - likely to have comparable performance with random forests
            - theoretically, it can find global optima that are missed by greedy expansion of CART algorithm
    - feature importance
        - cool feature importance heat map for MNIST dataset to verify that the model indeed is looking at the pixels in the center
5. Boosting
    - train weak learners sequentially
    - training can't be parallelized but inference can be
    - AdaBoost 
        - update weights of training samples in training each classifier
        - give higher weight to mis-classified samples from Ensemble[1:i-1] while training ith classifier
        - decay weights of predictions of later classifiers during inference
    - Gradient Boosted Trees
        - minimize residual error from previous prediction
        - learning rate = contirbution of subsequent classifiers
        - regularization
            - early stopping, learning rate
6. Stacking
    - instead of hard voting, train another model to aggregate the predictions of weak learners
    - even possible to create a "neural network" where each node is a random forest and a layer makes predictions using previous layer's output
        - split training data into N sets to train N layers seperately (not too much data is needed to train a weak learner anyway)

# References

- [1] Hands on ML: https://github.com/ageron/handson-ml3