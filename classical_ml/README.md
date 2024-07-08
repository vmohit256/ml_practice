
# Concepts

1. Bias/Variance tradeoff
    - Total errors in generalization = (error due to bias) + (error due to variance) + (intrinsic error in the dataset) [1]
        - error due to bias = error due to wrong assumptions about data (eg: linear regression on circular boundary) = error due to poor / underfitting of training data
        - error due to variance = error due to model being *very* sensitive to the training data / process and hence fitting noise inside it = error due to overfitting on training data
        - intrinsic error = even the best most optimal algorithm can not reduce error more than this on the dataset
    - "Tradeoff" may not be the right way to think about this, especially in modern deep learning models [2]
        - increase model size -> reduce bias without affecting variance (assuming it is properly regularized)
        - add more training data -> reduce variance without affecting bias (TODO: not very clear why and what are hidden assumptions in this)
        - techniques like bagging, voting aggregator, etc. reduce variance without affecting bias
    - It is possible to have both high-bias and high-variance [example](https://youtu.be/SjQyLhQIXSM?si=fTX1-Hq3oj0qGioT&t=441) [2]
        - example in video is contrived but happens often in high-dimensions with regions of high-bias and high-variance sprinkled everywhere
    - Basic recipe for model dev: [2]
        1. High bias / large training error -> bigger network, train longer, (different architecture / model)
        2. Low bias AND High variance -> get more data, stronger regularization, (different architecture / model)
    - Intuition: result of voting on 1000 biased coin toss to reduce prediction variance while keeping bias the same

# References

- [1] Hands on ML: https://github.com/ageron/handson-ml3
- [2] Andrew NG videos ([Bias/Variance (C2W1L02)](https://www.youtube.com/watch?v=SjQyLhQIXSM&t=23s&ab_channel=DeepLearningAI), [Basic Recipe for Machine Learning (C2W1L03)](https://www.youtube.com/watch?v=C1N_PDHuJ6Q&ab_channel=DeepLearningAI)) 

