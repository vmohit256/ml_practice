
# Papers / Ideas

## Surveys

- [T5] [Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer](https://arxiv.org/pdf/1910.10683)
    - convert every NLP problem into a text-to-text problem

## Architecture

- [Attention OG] [Attention Is All You Need](https://arxiv.org/pdf/1706.03762) (2017)
    - Main experiment problem: Machine Translation
    - Encoder-Decoder architecture with attention mechanism
        - encoder takes input sparse (w_1, w_2, ..., w_n) and converts it into dense representation (z_1, z_2, ..., z_n)
        - decoder takes dense representation and generates output sparse (y_1, y_2, ..., y_m)
        - both encoder and decoder have 6 layers each
        - embedding dimension, d_model = 512
    - encoder
        - input = token embeddings + positional encodings
        - output of hidden layer with contextual embeddings
        - layer architecture
            - Multi-Head Self-Attention
                - not masked. Every word can see every other word
                - queries, keys, and values all come from the same input
            - Residual Connection
            - Layer Normalization
                - LayerNorm(x + SubLayer(x))
            - Feed Forward Network
                - FFN(x) = ReLU(x W_1 + b_1) W_2 + b_2
                - appied independently to each position
            - Residual Connection + Layer Normalization
    - decoder (causal / auto-regressive)
        - input: output token embeddings shifted 1 position to the right, encoder output, positional encodings
        - layer architecture
            - (decoder only) Multi-Head Self-Attention  // TODO: why is this layer present? Presumably because this one attends to decoder only and the next one attends to encoder only. So there is a separate layer for each instead of a single layer that attends to both. 
                - only on previous words and not encoder output
                - each word can only see previous words
                - queries, keys, and values come from decoder previous words only. No encoder output is used here
            - residual connection + layer normalization
            - (encoder-decoder both) Multi-Head Self-Attention
                - on both encoder output and previous words
                - queries come from previous decoder layer,
                - keys and values come from encoder output
                - intuition is for the decoder to attend to and incorporate information from the encoder
            - residual connection + layer normalization
            - Feed Forward Network
            - residual connection + layer normalization
        - final is linear layer with softmax
    - attention
        - d_k = d_v = d_model / h = 64 (h=8 heads)
        - scaled dot-product attention
            - MaskedAttention (X_O Wq_i, X_I Wk_i, X_I Wv_i) = (softmax((X_O Wq_i) (X_I Wk_i)^T / sqrt(d_k) + Mask) (X_I Wv_i))
            - X_I is N_I x d_model matrix representing input to the layer. N_I = input sequence length. It is maximum length of the sequence given input to the layer. Paddings are masked and future words are masked (in case of decoder)
            - Wq_i is d_model x d_k matrix representing matrix that transforms input to query
                - X_O is N_O x d_k matrix representing subset of input sequence that is used to calculate output sequence. N_O = output sequence length
                    - for the layer that takes both encoder output and previous words, N_I = max_encoder_input_length + max_decoder_input_length and N_O = max_decoder_input_length
                    - only use decoder emebeddings as queries
                - X_O Wq_i is N_O x d_k matrix representing queries for each element in the output sequence
            - Wk_i is d_model x d_k matrix representing matrix that transforms input to key
                - X_I Wk_i is N_I x d_k matrix representing keys for each element in the input sequence
            - attention weights: 
                - A = (X_O Wq_i) (X_I Wk_i)^T . M / sqrt(d_k) is N_O x N_I matrix representing attention weights for each element in the sequence
                - M masks the future words and paddings
                - A_lm = (row l of X_O Wq_i) . (column m of (X_I Wk_i)^T) / sqrt(d_k) + M_lm
                    - (row l of X_O Wq_i) is 1 x d_k matrix representing the query for l-th element in the output sequence
                    - (column m of (X_I Wk_i)^T) is d_k x 1 matrix representing the key for m-th element in the input sequence
                    - M_lm -infinity if l^th shouldn't be attending to m^th element. Softmax will make these weights 0
                    - A_lm is unnormlized attention weight that l^th output pays to m^th input
            - (X_I Wv_i) is N_I x d_v matrix representing values for each element in the input sequence that it can contribute to any element of output sequence that attends to it
            - head_i = softmax(A) (X_I Wv_i) is N_O x d_v matrix representing output of the layer for this head
                - (softmax(A) (X_I Wv_i))_xy = sum_m softmax(A)_xm (X_I Wv_i)_my
                    - this is taking weighted average of value vectors depending on attention weights
        - MultiHead Self Attention
            - Concat(head_1, head_2, ..., head_h) W^O is h * d_v x d_model matrix to combine output of all heads
    - weight tying: same embedding matrix used for both encoder and decoder
    - positional encodings
        - non-learnable and fixed sin and cos functions of different frequencies
        - added to input embeddings
        - designed so that PE_pos+k = W * PE_pos, i.e. positional embeddings can be tanformed to any other position by linear trasnformations only
        - fixed sin-based positional embeddings may allow for generalization to longer sequences not present in training data
        - learned embeddings tend to look like these fixed embeddings naturally
    - interpretability
        - attention heads are clearly performing different functions relating syntactic and semantic structure of the sentence // TODO: explore this literature 
    - training
        - datasets
            - WMT 2014 English-German
                - 4.5 million sentence pairs
                - 37k BPE vocabulary (shared source and target)
            - WMT 2014 English-French
                - 36 million sentence pairs
                - 32k word-peice vocabulary (shared source and target)
        - hardware
            - 8 NVIDIA P100 GPUs
            - 12 hours (100k steps total and 0.4 seconds per step) for small models
            - 3.5 days (300k steps total and 1.0 seconds per step) for big models
        - hyper params
            - 25000 tokens per batch
            - Adam optimizer with beta1=0.9, beta2=0.98, epsilon=10^-9
            - lrate schedule, learning rate = d_model^-0.5 * min(step_num^-0.5, step_num * warmup_steps^-1.5)
                - slowly increase learning rate for first warmup_steps (=4000) steps and then decrease it proportional to inverse square root of step number
            - regularization
                - dropout rate = 0.1 to each sublayer just before adding residual connection and then layer normalization
                - label smoothing = 0.1  // TODO: read up on this
                    - flip 10% of the one-hot target vector to 0.1
        - results
            - had better BLEU score than previous state-of-the-art models
        - ablation study and observations
            - bigger models are better
            - tuning h, dk, dv is important given size is fixed
            - using fixed positional encodings is as good as learned ones



## BERT-based Models

- [BERT OG] [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/pdf/1810.04805)
    - feature based: use pre-trained model's output as static features for downstream tasks
    - fine tuning: fine-tune all parameters of pre-trained model on downstream task
    - pretraining
        - architecture
            - same as attention is all you need with no masking
            - L = num of transformer layers, H = embedding size, feed forward size = 4*H, A = num attention heads
            - BERT BASE (L=12, H=768, A=12, Total Parameters=110M)  // same size as GPT
            - BERT LARGE (L=24, H=1024, A=16, Total Parameters=340M)
            - word piece tokenizer with 30k token vocabulary
            - input / output representations
                - able to represent single sentence or a pair of sentences
                - first token is always [CLS] (classification token)
                - [CLS] <sentence-1> [SEP] <sentence-2> [SEP] (sentence 2 is optional)
                - add learned embeddings for segment ids (0 for sentence 1, 1 for sentence 2)
                    - input embeddings = token embeddings + segment embeddings + positional embeddings
        - masked language model
            - 15% of input tokens are masked, 80% of masked tokens are replaced with [MASK], 10% of masked tokens are replaced with random token, 10% of masked tokens are left as is
                - [MASK] will never appear during fine tuning. Thats why 20% samples don't have it so the model doesn't get confused during fine tuning
        - next sentence prediction
            - binary classification: 50% of the time, sentence 2 is the actual next sentence of sentence 1, 50% of the time, sentence 2 is a random sentence from the corpus
            - shown very beneficial for QA and NLI tasks
            - [CLS] token's output is used for the classification task
                - [CLS] not a meaningful sentence representation without fine tuning and presence of a sentence pair
        - data
            - BooksCorpus (800M words) + English Wikipedia (2.5B words) (include on text passages. Ignore lists, tables, etc.)
    - fine tuning
        - tune all parameters end-to-end
        - not very expensive. Most reported tasks finish in a few hours on a single GPU
        - input wiring for different tasks
            - sentence pairs in paraphrasing
            - hypothesis-premise pairs in entailment
            - question-passage pairs in question answering
            - a degenerate text-∅ pair in text classification or sequence tagging
        - output wiring for different tasks
            - [CLS] token's output for classification tasks
    - experiments
        - beats all existing baselines on 11 NLP tasks
        - GLUE (General Language Understanding Evaluation)
            - single sentence
                - CoLA The Corpus of Linguistic Acceptability: "They drank the pub dry." v/s "They drank the pub.". Is the sentence grammatically correct?
                - SST-2 The Stanford Sentiment Treebank. Predict movie review sentiment
            - similarity and paraphrasing
                - MRPC Microsoft Research Paraphrase Corpus. Predict if two sentences are paraphrases
                - QQP Quora Question Pairs. Predict if two questions are semantically equivalent
                - STS-B Semantic Textual Similarity Benchmark. Predict similarity score between two sentences. 
                    - dissimilar: "A man is smoking" v/s "A man is skating."
                    - similar: "A plane is taking off" v/s "An air plane is taking off"
            - inference
                - MNLI Multi-Genre Natural Language Inference. Predict entailment, contradiction, or neutral relationship between two sentences
                - QNLI The Stanford Question Answering Dataset. question-paragraph pairs, where one of the sentences in the paragraph (drawn from Wikipedia) contains the answer to the corresponding question (written by an annotator).
                - RTE The Recognizing Textual Entailment (RTE) datasets come from a series of annual textual entailment challenges
                - WNLI The Winograd Schema Challenge (Levesque et al., 2011) is a reading comprehension task in which a system must read a sentence with a pronoun and select the referent of that pronoun from a list of choices
            - batch size 32, 3 epochs, learning rate tuned from {5e-5, 4e-5, 3e-5, 2e-5} on dev set
            - BERT large was unstable on small datasets so pick best from randomized restarts on shuffled data
            - BERT large always outperformed BERT base, especially when fine tuned on small datasets
        - SQuAD (Stanford Question Answering Dataset)
            - 100k crowdsourced question-paragraph pairs
                - given question and paragraph, predict start and end token of the answer in the paragraph
            - plugin question as sentence A and paragraph as sentence B
            - introduce two new tokens [START] and [END] to predict start and end of the answer
                - training: cross entropy loss on correct start and end token locations
                - inference: pick i, j (i < j) that maximizes S . T_i + E . T_j
            - SQuAD v2
                - adds possibility of no answer
                - in case of no answer, train S.C and E.C to maximize at [CLS] token
                - inference: s_null = S . C + E . C and pick i, j that maximizes S . T_i + E . T_j or s_null, whichever is higher
        - SWAG (Situations With Adversarial Generations)
            - 113k sentence pairs
            - given a sentence, predict the most plausible continuation among 4 choices
            - plugin sentence as sentence A and candidate continuation as sentence B
            - use output of [CLS] to score each candidate  // TODO: what exactly is the loss function?
    - ablation study
        - removing NSP hurts performance significantly on QNLI, MNLI, and SQuAD
        - left to right always performs worse than bidirectional
        - bigger models are better on all tasks, even when training data is very small
        - feature based approaches also work, though not as well as fine tuning
            - pick final 2-3 layers of BERT and use their output as features for training a new model from scratch on these static precomputed features
                
            

## Big Pretraining

## RLHF

## Fine Tuning

## Multi-Modal Models

- CLIP

## Distillation

# Links

