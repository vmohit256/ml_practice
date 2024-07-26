from collections import Counter

"""
This class builds a local vocabulary using the Hugging Face BERT tokenizer library.
This is useful for using the same tokenizer as bert for tokenizing text data.
"""
class LocalVocabHF:
    """
    train_data:
        Already tokenized training data like:
        imdb = load_dataset("imdb")
        imdb_train = imdb_train.map(lambda x: {'text': custom_standardization(x['text'])})
        tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
        imdb_train = imdb_train.map(lambda x: tokenizer(x['text'], padding='max_length', truncation=True, max_length=512), batched=True)
    """
    def __init__(self, train_data) -> None:
        train_global_id_counts = Counter()
        for example in train_data:
            train_global_id_counts.update(example['input_ids'])
        print (f"There are {len(train_global_id_counts)} token_ids in local vocab")
        self.train_global_id_counts = train_global_id_counts
        
        self.global_id_to_local_id = {token_id: id+1 for id, token_id in enumerate(train_global_id_counts.keys())}
        self.local_id_to_global_id = {v:k for k,v in self.global_id_to_local_id.items()}

        self.train_local_id_counts = {self.global_id_to_local_id[k]:v for k,v in train_global_id_counts.items()}

        assert '<UNK>' not in self.global_id_to_local_id
        self.global_id_to_local_id['<UNK>'] = 0

    def __len__(self):
        return len(self.global_id_to_local_id)
    
    def get_local_id_for_global_id(self, global_id):
        return self.global_id_to_local_id.get(global_id, 0)
    
    def get_global_id_for_local_id(self, local_id):
        return self.local_id_to_global_id.get(local_id, -1)
    
    def get_frequent_local_ids(self, min_term_freq):
        return {k:v for k,v in self.train_local_id_counts.items() if v >= min_term_freq}
