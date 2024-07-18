
# Unstructured Notes

## Section-1: Text Processing

- Regular Expressions
    - applications
        - extract info: dates, times, emails, phone numbers
        - validate correctness of data. eg: email, phone number
        - tokenizer built using optimized DFA regex
- Tokenization
    - what counts as a word? -> depends on application
        - Understand the dataset
            - Motivation of data creation, situation of data collection, language variety (language, dialect, slang, etc.), speaker demographics, collection process, annotation process, distribution (copyright / IP restrictions, etc.)
        - Understand the task
            - punctuations / special characters: useful for $45.55, 01/01/2020, abc@xyz.com, etc.
            - lemmatization
                - useful for inverted index
            - depends on language
                - for chinese, may use the characters directly
                - for japanese, the tokenizer is very complex and is a separate trained model by itself
        - aim to balance between
            - tokenizing too much: deep learning model would invest too much time in learning that most combinations are not useful and only some are useful. Given a sequence of characters like: 'n', 'e', 'w', ' ', 'y', 'o', 'r', 'k', there are catalan number of unique ways to split it. But only 3-4 are useful. So, the model would have to learn that most of the splits are not useful. This is a waste of time and resources.
            - tokenizing too little: if "to be or not to be" is a single token then it appears very infrequently in the corpus and so would have less data to learn its meaning. Eg: say the task is machine translation. The sentence "to be or not to be" appears only 2-3 times in training data with long translations. It will be difficult to learn exactly why it was translated that way with jus tthese samples. But, words like "to", "be", etc. appear a lot and their translation meaning could be generalized and useful for the bigger sentence "to be or not to be" as well.
    - Herdan/Heap's law: `V = k * N^b`
        - for large corpus, `b` is between 0.67 and 0.75 sp vocab size grows fater than square root of corpus size
    - top-down (rule based)
        - simple lowercase, remove special characters, split on whitespace
        - nltk.regexp tokenize
        - Penn Treebank tokenization standard (hand-crafted rules)
    - bottom-up (unsupervised)
        - Byte Pair Encoding (BPE)
            - starting from individual characters, merge most frequent pair of sub-words
        - [Unigram Language Modelling](https://arxiv.org/pdf/1804.10959)
            - TODO: read up on botton-up tokenizers in more detail
- Word Normalization
    - convert USA, US, U.S.A., etc. to a normalized form, say, United States of America
        - looses information but useful if the lost information is not important for the task
            - positive example: aggressive normalization in inverted search index (drop stop words, case-folding, lemmatization, etc.)
            - negative example: in sentiment analysis, the capitalization of words is important. Eg: "I am not happy" vs "I am NOT happy"
    - case-folding
    - lemmatization
- Minimum Edit Distance
    - dynamic programming
    - Viterbi algorithm is a probabilistic extension of minimum edit distance
        - Instead of computing the minimum edit distance between two strings, Viterbi computes the maximum probability alignment of one string with another

## Section-2: N-gram Language Models

- Applications
    - large language models
    - correct grammar / spelling mistakes: Their are two midterms
    - speech recognition: I will be back soonish and not I will be bassoon dish
    - augmentative and alternative communication systems
- model
    - markov assumption on chain rule of conditional probability
    - MLE estimate: `P(w_i | w_{i-1}) = count(w_{i-1}, w_i) / count(w_{i-1})`
- linguistic phenomenon captured
    - syntactic
        - what comes after eat is usually a noun or an adjective
        - what comes after to is usually a verb
    - context in which the language is used. Eg: if the data is about personal assistant task, sentences may have high probability of starting with "I", as in, "I want to..."
    - cultural context. Eg: probability of "Chinese" might be higher than "English" for the sentence, "I am looking for a good _ restaurant"
- evaluation
    - extrinsic: improve performance on downstream task
    - intrinsic: perplexity
        - perplexity is the inverse probability of the test set, normalized by the number of words. Or log likelihood per word.
            - important to avoid contamination of training and test data
        - The test set should reflect the language we want to use the model for
        - perplexity as weighted average branching factor of a language model
            - TODO: undestand the intuitive link between this definition and the definition of perplexity as normalized inverse likelihood probability of the test set
        - connected to entropy. TODO: don't quite understand this
            - entropy is the average number of bits needed to encode a word
            - perplexity is 2^entropy
- unknown words
    - closed vocabulary: defined only when test set contains only known words
        - subword tokenizers like BPE are like this
    - open vocabulary
        - add `UNK` token in vocab
            - A language model can achieve low perplexity by choosing a small vocabulary and assigning the unknown word a high probability.
            - Language models are comparable (through perplexity) only if they have exact same vocabulary
- smoothing
    - shave off some probability mass from frequent events and give it to unseen events
    - laplace smoothing
        - p(w_i | w_{i-1}) = (count(w_{i-1}, w_i) + 1) / (count(w_{i-1}) + V)
        - add-k smoothing
            - p(w_i | w_{i-1}) = (count(w_{i-1}, w_i) + k) / (count(w_{i-1}) + kV)
            - k=1 moves lots of probability mass from frequent events to unseen events
            - tune k on validation set
    - back off: move to lower order model if higher order model has zero probability
        - need to shave off some probability mass from higher order model to give to lower order model to make sure the sum of probabilities is 1
        - Katz backoff, Good-Turing, Good-Turing backoff
            - P(w_i | w_{0:i-1}) = P'(w_i | w_{i-1}) if count(w_{0:i}) > 0 else alpha(w_{0:i-1}) * P(w_i | w_{1:i-1})
            - P' and alpha are picked so that the sum of probabilities is 1
            - many sophisticated variations of this. TODO: read up on them
        - Huge n-gram language model
            - efficiency is important: 4-8 bit quantized probabilities, use 64-biit hash ids instead of strings for words, store word strings in disk, store ngram in reverse tries
            - use of cache- keep only n-grams with count > k
            - entropy based pruning, approximate LM using bloom filters. TODO: what?
            - stupid back-off: relax the constraint that the sum of probabilities should be 1. Works well in practice. TODO: read up
    - interpolation: linear combination of higher and lower order models
        - learn weights on validation set
            - EM algorithm: fix ngram probabilities and learn interpolation weights. Then fix interpolation weights and learn ngram probabilities
    - absolute discounting
        - GOOD IDEA: split dataset 50:50 and compare counts for same ngrams in the held out set to identify correct discounting
            - observation: absolute discounting is a good model for the held out set
        - p(w_i | w_{i-1}) = (count(w_{i-1}, w_i) - d) / count(w_{i-1}) + lambda(w_{i-1}) * p(w_i | w_{i-1})
            - not too bad for high count n-grams but doesn't help much for low count n-grams
    - Kneser-Ney smoothing
        - Pcontinuation: I can’t see without my reading _. If bigram count is 0, then KONG (from HONG KONG) has more probability then glasses in unigram
            - P_KN(w_i | w_{i-1}) = max(count(w_{i-1}, w_i) - d, 0) / count(w_{i-1}) + lambda(w_{i-1}) * Pcontinuation(w_i)


# References

- https://web.stanford.edu/~jurafsky/slp3/
