
# Unstructured notes

- light weight reco ideas
    - recently viewed items
    - popular / hot products
- items bought together / complementary items
    - phone + phone cases + screen protectors
- similar items
    - show ads on pdp
- frameworks
    - content based filtering
        - user activity -> user profile -> recommend items similar to user profile
            - raw activity (queries, clicks, purchases, etc.)
            - affinities: category, price, brands, topics, etc.
            - embeddings in same space as items
    - collaborative filtering
        - discover novel unexplored recommendations
    - layered ranking
        - L1 (Retrieval): selection: High recall / low precision. Scalable and fast.
            - ANN retrieval. Compute offer -> embedding offline. At runtime, compute user embedding and find nearest neighbors.
            - topic modelling
        - L2 (Scoring): compute relevance score. 
            - High precision. Real-time. Needs to meet latency requirements.
            - Lots of features (user, item, user-item, etc.)
            - XGBoost, LightGBM, etc.
            - deep learning models
                - [Deep Interest Network for Click-Through Rate Prediction](https://arxiv.org/pdf/1706.06978)
                    - input features: user, item, user-item features and output is a click probability
                - [DeepFM: A Factorization-Machine based Neural Network for CTR Prediction](https://arxiv.org/pdf/1703.04247)
                - product embeddings
                    - fine-tuned BERT based models for textual features like title
                    - use image-text models for image features
                        - https://www.microsoft.com/en-us/research/blog/turing-bletchley-a-universal-image-language-representation-model-by-microsoft/
                        - https://arxiv.org/pdf/2102.05918
                        - https://arxiv.org/pdf/2103.00020
                - get user embeddings from product embeddings of items user has interacted with
        - L3 (Reranking): 
            - diversification of results (L2 might have very similar results in top-k based on relevance score only)
            - boost fresh trending content (like newly published youtube video that has potential to go viral)
            - remove click baits
            - multi-armed bandit / fast reinforcement learning. 
                - PROJECT IDEA: create tiktok like experience for wikipedia articles. Quick navigation of wikipedia data through left/right swipes
    - incorporate feedback from model deployed in prediction to continually / daily train it on interactions (active learning?)


# References

- [Frameworks to design recommendation system](https://developers.google.com/machine-learning/recommendation/overview)
- [XGBoost Learning to Rank Algorithms](https://xgboost.readthedocs.io/en/latest/tutorials/learning_to_rank.html)