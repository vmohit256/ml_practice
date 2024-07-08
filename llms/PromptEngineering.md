
# Types of Tasks

* Reasoning
    - [T1] Arithmetric reasoning (Ref:[P1] [P2])
        - "Sara has 31 red and 15 green balloons . Sandy has 24 red balloons . How many red balloons do they have in total ? "
        -  (1) SingleEq [Koncel-Kedziorski et al., 2015], (2) AddSub [Hosseini et al., 2014], (3) MultiArith [Roy and Roth, 2015], (4) AQUARAT [Ling et al., 2017], (5) GSM8K [Cobbe et al., 2021], and (6) SVAMP [Patel et al., 2021]
    - [T2] Commonsense Reasoning (Ref:[P1])
        - CommonsenseQA [Talmor et al., 2019] and StrategyQA [Gevaet al., 2021]
        - "Sammy wanted to go to where the people were.  Where might he go? Options: A, race track, B. desert, C. populated areas, D. apartment"
    - [T3] Symbolic reasoning (Ref:[P1])
        - Last Letter Concatenation and Coin Flip [Wei et al., 2022]
        - "A coin is heads up. Whitney flips the coin. Erika does not flip the coin. Tj does not flip the coin. Benito flips the coin. Is the coin still heads up? Note that \"flip\" here means \"reverse\"."
    - [T4] Logical Reasoning (Ref:[P1])
        - BIG-bench effort [Srivastavaet al., 2022]: Date Understanding and Tracking Shuffled Objects
        - "Alice, Bob, and Claire are playing a game. At the start of the game, they are each holding a ball: Alice has a orange ball, Bob has a white ball, and Claire has a blue ball. \n\nAs the game progresses, pairs of players trade balls. First, Alice and Bob swap balls. Then, Bob and Claire swap balls. Finally, Alice and Bob swap balls. At the end of the game, Bob has the "
    - [T5] Game of 24 (use 4 numbers and basic arithmetic operations (+-*/) to obtain 24) [P4]
    - [T6] Creative writing [P4]
        - input is 4 random sentences and the output should be a coherent passage with 4 paragraphs that end in the 4 input sentences respectively.
        - measuring coherence:
            - take average of 5 samples of GPT-4 zero shot scores from 1 to 10 (zero shot + self consistency)
            - ask human judges to pairwise evaluate coherence between A v/s B in a blind study
    - [T7] [Mini 5x5 crossword](https://www.goobix.com/crosswords/0505/) [P4]
    - [T15] Chess Move Prediction (predict the best next move in a game of chess, given the first 14 moves of a chess game between two chess grand-masters described in PGN notation) [P12]
* Planning / Decision making: step-by-step feedback and environment interaction
    - [T12] ALFWorld (Shridhar et al., 2020b)
        - synthetic world text based game
        - "It includes 6 types of tasks in which an agent needs to achieve a high-level goal (e.g. examine paper under desklamp) by navigating and interacting with a simulated household via text actions (e.g. go to coffeetable 1, take paper 2, use desklamp 1)."
    - [T13] WebShop (Yao et al., 2022)
        - online shopping website environment with 1.18M real-world products and 12k human instructions. 
        - requires an agent to purchase a product based on a user instruction (e.g. “I am looking for a nightstand with drawers. It should have a nickel finish, and priced lower than $140”) through web interactions (e.g. search “nightstand drawers”, choose buttons such as “color: modern-nickel-white” or “back to search”). 
* [T9] Big-Bench Hard (BBH) (Suzgun et al., 2022), MATH (Hendrycks et al., 2021) ([code and data](https://github.com/suzgunmirac/BIG-Bench-Hard)) [P6]
    - ensembles of mostly reasoning tasks that are challenging for LLMs
    - MATH contains math problems from school/university. Like: Suppose a and b are positive real numbers with a > b and ab = 8. Find the minimum value of (a^2 + b^2) / (a - b)
        - Contains these seven subjects: Prealgebra, Algebra, Number Theory, Counting and Probability, Geometry, Intermediate Algebra, and Precalculus
    - BBH task descriptions:
        - Boolean Expressions: {"input": "not True or False or ( False ) is", "target": "False"}
        - Causal Judgment. Given a short story (involving moral, intentional, or counterfactual analysis), determine how a typical person would answer a causal question about the story. 
            - "A machine is set up in such a way that it will short circuit if both the black wire and the red wire touch the battery at the same time. The machine will not short circuit if just one of these wires touches the battery. The black wire is designated as the one that is supposed to touch the battery, while the red wire is supposed to remain in some other part of the machine. One day, the black wire and the red wire both end up touching the battery at the same time. There is a short circuit. Did the black wire cause the short circuit?\nOptions:\n- Yes\n- No" -> No
            - "The CEO of a company is sitting in his office when his Vice President of R&D comes in and says, 'We are thinking of starting a new programme. It will help us increase profits, but it will also harm the environment.' The CEO responds that he doesn't care about harming the environment and just wants to make as much profit as possible. The programme is carried out, profits are made and the environment is harmed. Did the CEO intentionally harm the environment?\nOptions:\n- Yes\n- No" -> Yes
            - "Ned has a new motorboat. When Ned turns the key, the motorboat starts if either the gear is in neutral or the motor is in the lock position. Today, the gear is in neutral, and the motor is not in the lock position. Ned checks the motor to see if it is in the lock position. He changes its position, and he puts it in the lock position. Because the motorboat would start if either the gear is in neutral or the motor is in the lock position, the motorboat starts when Ned turns the key. Did the motorboat start because Ned changed the position of the motor?\nOptions:\n- Yes\n- No" -> No
        - Date Understanding: “The concert was scheduled to be on 06/01/1943, but was delayed by one day to today. What is the date yesterday in MM/DD/YYYY?”
        - Disambiguation QA: "In the following sentences, explain the antecedent of the pronoun (which thing the pronoun refers to), or state that it is ambiguous.\nSentence: The surgeon warned the patient that he needed to get more rest.\nOptions:\n(A) The surgeon needed more rest\n(B) The patient needed more rest\n(C) Ambiguous" -> (B) {Note: It should be (C) right!!!!???}
        - Dyck Languages: "Complete the rest of the sequence, making sure that the parentheses are closed properly. Input: < [ ] { < ( ) > } [ ] ( { }" -> ") >"
        - Formal Fallacies Syllogisms Negation: "\"Is Siri a stepsister of Mary? Is Susan related to Kate? In large families, it is sometimes difficult to keep track of all one's relatives. The following argument seeks to clarify some such relations: To start with, not being a niece of Shirley is sufficient for not being a workmate of Sharita. Now, everyone who is a stepsister of Nichole is a workmate of Sharita, too. We may conclude: Being a niece of Shirley is necessary for not being a stepsister of Nichole.\"\nIs the argument, given the explicitly stated premises, deductively valid or invalid?\nOptions:\n- valid \n- invalid" -> "invalid" (Damn this is hard! Makes sense that the sota from reprompting paper has 56.8% accuracy, i.e. only slightly better than random guess)
        - Geometric Shapes: "This SVG path element \<path d=\"M 28.86,7.40 L 53.23,2.40 M 53.23,2.40 A 24.88,24.88 61.94 0,1 46.23,25.21 L 28.86,7.40\"/\> draws a\nOptions:\n(A) circle\n(B) heptagon\n(C) hexagon\n(D) kite\n(E) line\n(F) octagon\n(G) pentagon\n(H) rectangle\n(I) sector\n(J) triangle" -> (I) sector (wow! 73% accuracy on this dataset is pretty amazing!)
        - Hyperbaton (Adjective Ordering): adjective ordering: "Which sentence has the correct adjective order:\nOptions:\n(A) Egyptian tan large smoking archaic square match\n(B) large archaic square tan Egyptian smoking match" -> (B)
        - Logical Deduction: Deduce the order of a sequence of objects based on the clues and information about their spacial relationships and placements. "The following paragraphs each describe a set of five objects arranged in a fixed order. The statements are logically consistent within each paragraph. On a branch, there are five birds: a falcon, a raven, a cardinal, a hawk, and a crow. The cardinal is the second from the right. The hawk is to the right of the falcon. The raven is the second from the left. The crow is the rightmost.\nOptions:\n(A) The falcon is the rightmost\n(B) The raven is the rightmost\n(C) The cardinal is the rightmost\n(D) The hawk is the rightmost\n(E) The crow is the rightmost" -> (E)
        - Movie Recommendation: Given a list of movies a user might have watched and liked, recommend a new, relevant movie to the user out of the four potential choices user might have. "Find a movie similar to Dances with Wolves, The Shawshank Redemption, Apollo 13, Schindler's List:\nOptions:\n(A) Braveheart\n(B) Popeye\n(C) House II The Second Story\n(D) In China They Eat Dogs" -> (A) 
        - Multi-Step Arithmetic: Solve multi-step equations involving basic arithmetic operations (addition, subtraction, multiplication, and division). "((5 - -2 * 7 + -2) - (0 * 9 * -6 - -7)) =" -> "10"
        - Navigate: "If you follow these instructions, do you return to the starting point? Always face forward. Take 7 steps backward. Take 10 steps right. Take 4 steps forward. Take 1 step left.\nOptions:\n- Yes\n- No" -> No
        - Object Counting: "I have a couch, two beds, a fridge, an oven, a lamp, and a table. How many objects do I have?" -> 7
        - Penguins in a Table: Given a unique table of penguins (and sometimes some new information), answer a question about the attributes of the penguins. "Here is a table where the first line is a header and each subsequent line is a penguin:  name, age, height (cm), weight (kg) Louis, 7, 50, 11 Bernard, 5, 80, 13 Vincent, 9, 60, 11 Gwen, 8, 70, 15  For example: the age of Louis is 7, the weight of Gwen is 15 kg, the height of Bernard is 80 cm.  What is the name of the last penguin sorted by alphabetic order?\nOptions:\n(A) Louis\n(B) Bernard\n(C) Vincent\n(D) Gwen\n(E) James" -> (C)
        - Reasoning about Colored Objects: "On the table, there are two magenta paperclips, one gold booklet, three blue booklets, and three green booklets. If I remove all the paperclips from the table, how many magenta objects remain on it?\nOptions:\n(A) zero\n(B) one\n(C) two\n(D) three\n(E) four\n(F) five\n(G) six\n(H) seven\n(I) eight\n(J) nine\n(K) ten\n(L) eleven\n(M) twelve\n(N) thirteen\n(O) fourteen\n(P) fifteen\n(Q) sixteen"
        - Ruin Names: Given an artist, band, or movie name, identify a one-character edit to the name that changes the meaning of the input and makes it humorous. "Which of the following is a humorous edit of this artist or movie name: 'nine inch nails'?\nOptions:\n(A) nine ionch nails\n(B) nine inch sails\n(C) nine inch qnails\n(D) nine isch nails" -> (B)
        - Salient Translation Error Detection: Given a source sentence written in German and its translation in English, determine the type of translation error that the translated sentence contains.
        - Snarks. Given two nearly-identical sentences, determine which one is sarcastic.
        - Sports Understanding. Determine whether a factitious sentence related to sports is plausible.
        - Temporal Sequences. Given a series of events and activities a person has completed in the course of a day, determine what time, during the day, they might have been free to perform another activity
        - Tracking Shuffled Objects. Given the initial positions of a set of objects and a series of transformations (namely, pairwise swaps) applied to them, determine the final positions of the objects
        - Web of Lies. Evaluate the truth value of a random Boolean function expressed as a natural-language word problem.
        - Word Sorting. Given a list of words, sort them lexicographically
* [T8] Instruction induction tasks proposed in Honovich et al. (2022). An ensemble of tasks. [P5]
    - Knowledge: Larger Animal: Write the larger of the two given animals. koala, snail → koala
    - Linguistic: Negation: Negate the input sentence. Convert to passive voice, write a synonym, etc.
    - Sentiment classification (positive / negative movie review)
* Text Summarization
* Text Generation
* Question Answering
    - [T10] [HotPotQA (Yang et al., 2018)](https://arxiv.org/pdf/1809.09600) [P9]
        - https://hotpotqa.github.io/
            - good dataset to evaluate RAG systems
            - give random a -> b entities by scraping first paragraphs to human labellers
            - they try to generate 3 types of questions multi-hop reasoning questions along with actual answers and supporting snippets:
                - Bridge entity question: "when was the singer and songwriter of Radiohead born?". Here a -> b is Radiohead (Band) --- lead singer ---> "Thom Yorke" with "b" being bridge entity
                - Comparison question: comparing a and b like “Who has played for more NBA teams, Michael Jordan or Kobe Bryant?”
                - Yes/No: question involving a and b: “Are Iron Maiden and AC/DC from the same country?”
        - paper describes a bunch of cleaning methodologies to remove easy / bad questions and isolate good multi-hop questions
        - insights about the wikipedia data
            - hyper-links in the Wikipedia articles often naturally entail a relation between two entites in the context
            - the first paragraph of each article often contains much information that could be queried in a meaningful way
            - entities like countries are frequently referred to in Wikipedia, but don’t necessarily have much in common with all incoming links
    - [T11] [FEVER (Thorne et al., 2018)](https://arxiv.org/pdf/1803.05355) [P9]
        - contains claims like: “Fiji’s largest island is Kauai.” and truth value (eg: False) along with supporting evidence snippet from wikipedia like "Viti Levu, the largest island, covers about 57% of the nation's land area" from geography of fiji wiki article
        - labels are supported, refuted, or not enough information. Evidence is present in first 2 cases.
        - stage-1: claim generation
            - labeller is given random sentence and a list of linked entities surrounding it
            - generate claims that are non-trivial (i.e. not directly inferrable from the source sentence)
            - generate false mutations of it using: paraphrasing, negation, substitution of an entity/relation with a similar/dissimilar one, and making the claim more general/specific
        - stage-2: claim labelling
            - get consensus from labellers. More details in the paper
* Text Classification
* Role Playing
* Code Generation / programming
    - [T14] [HumanEval 2021](https://arxiv.org/pdf/2107.03374v2) ([dataset](https://github.com/openai/human-eval/blob/master/data/HumanEval.jsonl.gz))
        - generate python function from docstring
        - used for codex (finetuned gpt3). get training data from github.
        - includes sandbox for testing
        - sampling 100 samples from codex and picking one that works most of the time (does test data have training samples?)
        - use functional equivalence to test correctness or human judgments


# Papers / Ideas

* [P1] [Large Language Models are Zero-Shot Reasoners](https://arxiv.org/pdf/2205.11916) ([code and datasets](https://github.com/kojima-takeshi188/zero_shot_cot/)) [NIPS 2022]
    - summary: just adding "Lets think step-by-step" in prompt helps for reasoning tasks
    - on arithmetic reasoning, cot makes a huge difference. Much more than few shot examples.
    - "the performance drastically increases with chain of thought reasoning, as the model size gets bigger. When the model size is smaller, chain of thought reasoning is not effective. large-scale models clearly demonstrate better reasoning"
    - used greedy decoding (eg: set temperature=0) (though sampling temperature!=0 in logs???)
* [P2] [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903) [NIPS 2022]
    - contains links to a bunch of datasets. They are similar to [P1]
    - shows that cot is effective on reasoning tasks. Improvments are higher on benchmarks requiring multi-step reasoning
* [P3] [SELF-CONSISTENCY IMPROVES CHAIN OF THOUGHT REASONING IN LANGUAGE MODELS](https://arxiv.org/pdf/2203.11171) [ICLR 2023]
    - similar datasets and authors as [P1] and [P2]
    - "We also show self-consistency significantly outperforms sample-and-rank, beam search, ensemble-based approaches, and is robust to sampling strategies and imperfect prompts."
    - don't sample greedily, instead sample with randomness (eg: set temperature=0.5) a bunch of times and take majority vote as the final answer
* [P4] [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/pdf/2305.10601) [NIPS 2023] ([code](https://github.com/princeton-nlp/tree-of-thought-llm/tree/master))
    - in Game of 24, GPT-4 with cot is 4% but tree of thought success rate is 74%. Similar big improvments in other tasks too
    - 4 steps:
        1. thought decomposition: hand-crafted for problem (next word in crossword, next paragraph in creative writing, etc.)
        2. thought generator: random sampling from LLM
        3. state evaluator: write LLM prompt to: (i) assign value (1 to 10, high/medium/low, etc.), or (ii) vote on which state is best
        4. search algorithms: BFS or DFS. 
* [P5] [LARGE LANGUAGE MODELS ARE HUMAN-LEVEL PROMPT ENGINEERS](https://arxiv.org/pdf/2211.01910) ([code](https://github.com/keirp/automatic_prompt_engineer)) [ICLR 2023]
    - human prompt and LLM prompt performance is very similar
* [P6] [Reprompting: Automated Chain-of-Thought Prompt Inference Through Gibbs Sampling](https://arxiv.org/pdf/2305.09993) [ICML 2024]
    - jump in accuracy is definitely significant as compared to cot
    - automation in prompt generation is very attractive
    - Formal structure of a CoT prompt
        - m: textual message that instructs the model to generate step-by-step solution
        - series of demonstrations. Each demonstration "i" is a triplet (x_i, z_i, y_i)
            - x_i: input to the model
            - z_i: recipe. step by step approach used to reach the final answer y_i
            - y_i: final answer
            - Good points: these examples serve two purposes: 
                - explain the intent of the question unambiguously
                - provides step-by-step guidances on the demonstration for the model to condition on and emulate in its response
        - x: actual input whose output we want
        - y, z: final output and recipe generated the model
    - This paper optimizes for the recipes (i.e. z_is) that works best on a given dataset after having fixed other parts of the prompt, i.e. m and (x_i, y_i)
* [P7] [Faithful Reasoning Using Large Language Models](https://arxiv.org/abs/2208.14271) 
    - TODO: Couldn't understand this. Has some formalized notion of reasoning and uses it to obtain traces of reasoning fomr LLMs instead of direct answer. But doesn't cot already does it?
* [P8] [STaR: Bootstrapping Reasoning With Reasoning](https://arxiv.org/pdf/2203.14465)
    - Chain of thought reasoning can be baked into models via fine-tuning. For tasks with an answer key, example chains of thoughts can be generated by language models.
    - Tries to get around the downside of CoT that CoT requires lots of expensive tokens in form of reasoning. It would be good to bake reasoning directly into the model itself by fine tuning. They show it can perform as well as a 30x larger model that is directly fine-tuned on only input-output pairs.
    - TODO: investigate and compare with other fine-tuning methods
* [P9] [REACT: SYNERGIZING REASONING AND ACTING IN LANGUAGE MODELS](https://arxiv.org/pdf/2210.03629) ([code](https://react-lm.github.io/)) [ICLR 2023]
    - HotPotQA [T10] and FEVER [T11] datasets with questions only
    - Action space:
        1. search[entity]: returns first 5 sentences from the wikipage of the entity or else top-5 most similar wiki pages to the query entity
        2. lookup[string]: returns next sentence in the page containing the string (simulating CTRL+F)
        3. finish[answer]: finish the process and provide answer
    - compared these methods:
        - no external knowledge: zero shot, cot, cot-sc
        - action only: each step can only be one of the actions. No inner reasoning monologue allowed
        - react->cot: thought -> action -> thought -> action .... (truncate the chain at 5-7 steps and fall back to cot-sc at the end)
        - cot-sc->react: if majority voting of cot-sc has < n/2 votes, fallback to react
        - finetuning: TODO: not sure what this is
    - React doesn't do much better than cot! it has better performance but not by much
        - majority of cot errors are hallucinations where it just makes somthing up is it doesn't know the answer
        - majority of react errors are getting stuck at the next action. It doesn't know what to do so repeats previous thoughts.
            - errors in search results also derails it badly and it sometimes don't recover. A lot of errors are due to this
    - finetuning is easier in react v/s zs, cot, act (TODO: what does this mean?)
* [P10] [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/pdf/2303.11366) ([code](https://github.com/noahshinn/reflexion?tab=readme-ov-file))
    - has 3 models: actor, evaluator, self-reflection
        - environment provides external feedback
        - evaluator sees short-term, last k stpes, and provides internal feedback to self-reflection model
        - self-reflection encodes the reflective text in long-term memory
        - actor sees short-term memory (last k steps) and long-term memory and decides next action
        - loop finishes when evaluator is satisfied
    - task-1: decision making ([T12] ALFWorld (Shridhar et al., 2020b))
        - showed big improvements and almost solved the task completely in react+relexion v/s react only
    - task-2: question answering / reasoning ([T10] HotPotQA (Yang et al., 2018))
        - comparison between: cot only, react only, cot+reflexion, react+reflexion
        - show big improvments over baselines
    - task-3: programming 
        - again it performs better than SOTA (GPT-4)
    - repo contains all the eval code and runs
- [P11] [Demonstrate-Search-Predict: Composing retrieval and language models for knowledge-intensive NLP](https://arxiv.org/abs/2212.14024) ([code](https://github.com/stanfordnlp/dspy))
    * TODO: couldn't understand this paper. what is novel in this paper? It seems to be just RAG. 
- [P12] [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/pdf/2305.14325) ([code](https://github.com/composable-models/llm_multiagent_debate)) [ICML 2024]
    * Approach: in a round
        - multiple agents generate their responses
        - all responses are combined and passed to each agent for generating a new response
        - stop when they converge
    * Observations:
        - convergence is theoretically not guaranteed but they empirically found convergence in most cases
        - " we found that prompts that encouraged models to be more “stubborn’ based on their own solutions led to longer debates and better final solutions."
        - "we observed that language model agents were relatively "agreeable", perhaps due to RLHF"
        - "we found that while debates typically converged into single final answers, these answers were not necessarily correct. Despite answers being incorrect, language models would confidently affirm that their answer is correct and consistent with all other agent responses."
    * method is orthogonal to other strategies like cot, sc, self reflexion, scratch pad calculations, rag, etc.
    * Tasks: Arithmetic ( What is the result of 12+15*21+0-3*27?), GSM8K, Chess move prediction [T15]
    * more agents, more rounds, more stubborn prompts are better but are more expensive
    * comparison against: single agent, single agent+reflection, multi-agent+majority voting, multi-agent+debate
        * debate shows significant gains
    * to reduce cost, we can summarize an agent's response in debate format. Otherwise concatenating all agents responses become very expensive
- Adhoc opinionated tricks and observations: https://github.com/brexhq/prompt-engineering?tab=readme-ov-file#why-do-we-need-prompt-engineering
    * give all available information relevant to the task at hand
    * Hypothetical Document Embedding: for RAG, user query may be too short for the embeddings based retrieval to work well. Ask model to generate a document on the fly for the user query before doing RAG
    * Command grammars: give functions to models with names, definitions, usages, etc.
    * Markdown tables and json formats can be handled well by the model mostly
- [P13] [Augmented Language Models: a Survey](https://arxiv.org/pdf/2302.07842)
    * TODO: read this
- An OpenAI researcher's review of the prompt engineering literature: https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
    * [IMPORTANT] Few shot learning: choice of prompt format, training examples, and the order of the examples can lead to dramatically different performance
        * Majority label bias: exists if distribution of labels among the examples is unbalanced 
        * Recency bias: refers to the tendency where the model may repeat the label at the end
        * Common token bias: indicates that LLM tends to produce common tokens more often than rare tokens
        * Example selection tips:
            - Choose examples that are semantically similar to the test example using k-NN clustering in the embedding space (https://arxiv.org/abs/2101.06804)
            - select a diverse and representative set of examples. A method for doing this is here: https://arxiv.org/abs/2209.01975 . Creates a graph of samples where edges are k-NN and nodes are scored to promote diverse samples
            - TODO: investigate a bunch of papers cited on the blog for example selection
        * Example ordering tips:
            - order randomly to avoid majority label and recency bias
            - choose the order such that the model does not produce extremely unbalanced predictions or being overconfident about its predictions
    * Tips for writing instructions in the prompt
        - describe the task requirements in detail
        - be specific and precise
        - explain the desired audience
    * CoT is more useful for complicated reasoning tasks and big models
    * Alternative to self-consistency: 
        - randomly order examples
        - swap out human-generated rationales with machine generated ones randomly during trials
    * higher temperatures are more likely to generate incorrect rationales but correct final output
    * Prompts with demonstrations of higher reasoning complexity can achieve better performance
    * When separating reasoning steps, newline \n symbol works better than step i, period . or semicolon ;
    * Complexity-based consistency is to explicitly prefer complex chains among all the generations by taking majority vote among only top-k complex chains. 
        * a paper found that complex demonstrations improved performance on complex tasks but degraded performance on simpler tasks
    * Augmented LMs
        - for few shot closed book QA, ordering evidence -> question -> answer was found better than question -> evidence -> answer (probably due to separation between question and answer)
        - PoE > Noisy channel > RAG (TODO: what is this?)
        - asking the model to "retrieve" some knowledge about the question internally only before giving final answer, help improve performance
- Old open ai cookbook: https://cookbook.openai.com/articles/techniques_to_improve_reliability
    * Split complex tasks into simpler subtasks
    * Structure the instruction to keep the model on task
    * Ask for justifications of many possible answers, and then synthesize
    * Prompt the model to explain before answering
    * Generate many outputs, and then use the model to pick the best one
    * Least-to-most prompting: split reasoning tasks into smaller more reliable sub-tasks
    * Verifiers: Use a discriminator to reject bad generations and regenerate bad samples



# Links

- https://github.com/openai/evals
- https://cookbook.openai.com/articles/related_resources#papers-on-advanced-prompting-to-improve-reasoning
- Gibbs sampling:
    * https://stats.stackexchange.com/questions/10213/can-someone-explain-gibbs-sampling-in-very-simple-words
