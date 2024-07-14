# Introduction

This directory contains code for parsing and analyzing wikipedia snapshots. Code is structured as follows:

1. extract_wiki_snapshot_summaries.ipynb
    - it scans the full snapshot and extracts summary of a page that we care about: internal links, text length, categories, etc.
    - it is cpu intensive and takes ~8 hours on a 8 core machine
2. error_estimation.ipynb
    - it samples a few pages and tries to estimate various kinds of errors in the processed summaries by comparing against the fresh wikipedia page fetched using wikipedia api
3. prepare_structured_data.ipynb
    - it prepares easy to consume structured data like tsv files, dfs/bfs analysis on category / page graphs, etc. 
    - rest of the code uses this structured data only and not big json files created in previous steps

# Known Issues

1. Lots of internal links are present inside info boxes. These are not being parsed correctly right now. Eg: https://en.wikipedia.org/wiki/Chubby_Grigg
2. Templates aren't expanded my parser. So some category pages have their parent category links broken. Eg: https://en.wikipedia.org/wiki/Category:20th-century_establishments_in_Chile
    - this most commonly happens with categories having year in them

These issues are quantified in error_estimation.ipynb


# Planning

1. Visualize category labels using power bi
    - category -> number of pages, list of pages
    - number of categories, distribution of number of pages per category
    - 
2. Compute page rank to allow sorting by page importance
3. Try out label propagation using neo4j: https://neo4j.com/docs/graph-data-science/current/algorithms/label-propagation/

# Semantic Clustering

Problem statement: identify subsets of wikipedia that related to a specific user defined query like "all species of bears", "historic locations in frace", etc.

Motivation: there are various use cases
1. Create small subsets for practicing ML / NLP algorithms. Wikipedia as a whole is really big and difficult to work with. But if we can identify a small subset we care about then we can practice algorithms like the list below on them. Best part is that many manual labels like page category, year, etc. are relatively easy to extract.
    - Reference: https://web.stanford.edu/~jurafsky/slp3/
    - regular expressions, normalization, tokenization, spell check / edit distance
    - language models, word embeddings trainging / fine tuning
    - text classification, sentiment detection
    - part of speech tagging, named entity recognition, information extraction (relations, events, time)
    - machine translation, question answering, information retrieval 
    - compare different methods for a specific task on a target dataset: HMM, LSTMs, attention, CNNs, RNNs, prompt engineering, etc.
    - coreference resolution; discourse coherence; lexicons for sentiment, affect, and connotation; semantic role labelling and argument structure (TODO: find out what are these)
2. Fine tune generative language models on specific subsets to try and boost performance on a specific task for lower cost. Build chatbots prompted / tuned for a specific task (eg: cricket expert with access to all cricket facts in wikipedia. It bases its arguments / recommendations on wikipedia and avoids hallucinations and making up facts without basis)

## Approaches

### Simplest: map query to category(-ies) and pick articles within them

* Pros:
    - simplest and easiest as the labels already exist in the dataset
* Cons:
    - what if the specific category I want does not exist? Eg: all species of bears
    - what if the coverage of category tagging is low, i.e. many pages in that category are not tagged with it?
    - what if there are false positive, i.e. articles are wrongly categorized into the target category?

### Hierarchical Clustering 

Cluster subgraphs using various distance functions
1. Single linkage / complete linkage / average linkage
2. Agglomerative v/s divisive clustering
3. Distance functions:
    - number of cross links (weighted by page rank)
    - overlap of existing category labels across two clusters (intuition: try to put articles with same category in the same cluster)

### Graph Segmentation into Foreground and Background

1. Identify a few foreground articles that definitely belong in the query result
2. Identify some background articles that definitely don't belong
3. Compute a minimum cost graph cut that seperates foreground with background

### Cost Reduction

One common problem with any approach is that the size of the data may make it impractical. Possible solutions:
1. Locality detection + collapse localities -> smaller decomposed locality graph
    - detect localities using a crude but efficient method
    - merge localities into single super nodes and update edges / edge weights appropriately
2. Elect representatives: 
    - identify top-k representatives from the whole graph
    - minimize distance of any node from its nearest representative node. 
        * Experiment with different distance functions
        * Add regularization in cost function to avoid neglect of particular localities / remote subset of nodes
    - keep only representatives for segmentation and collapse other nodes into edge weights
    - propagate labels from representatives to all other nodes using some method

# PowerBI App

The power bi app helps explore the data.
