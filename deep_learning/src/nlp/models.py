
from torch import nn
import torch

class NBWVanillaModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, dropout=None):
        super(NBWVanillaModel, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.dropout = dropout
        if type(dropout) == tuple:
            dropout1, dropout2 = dropout
        else:
            dropout1 = dropout2 = dropout
        if self.dropout is not None:
            self.dropout1 = nn.Dropout(dropout1)
        self.global_avg_pool = nn.AdaptiveAvgPool1d(1)  # Global average pooling
        if self.dropout is not None:
            self.dropout2 = nn.Dropout(dropout2)
        self.fc = nn.Linear(embed_dim, 1)  # Output layer for binary classification

    def forward(self, text):
        # text: [batch_size, seq_length]
        embedded = self.embedding(text)  # [batch_size, seq_length, embed_dim]
        if self.dropout is not None:
            embedded = self.dropout1(embedded)
        # Permute `embedded` to apply pooling across the embedding dimension
        embedded = embedded.permute(0, 2, 1)  # [batch_size, embed_dim, seq_length]
        pooled = self.global_avg_pool(embedded)  # [batch_size, embed_dim, 1]
        pooled = pooled.squeeze(2)  # [batch_size, embed_dim]
        if self.dropout is not None:
            pooled = self.dropout2(pooled)
        return torch.sigmoid(self.fc(pooled))  # Apply sigmoid activation


"""
This classifier takes input embeddings from cls token of a BERT based model
and applies a linear layer to predict the class label.
"""
class FF_CLS_Classifier(nn.Module):
    def __init__(self, embed_dim, dropout=None):
        super(FF_CLS_Classifier, self).__init__()
        self.dropout = dropout
        if type(dropout) == tuple:
            dropout1, dropout2 = dropout
        else:
            dropout1 = dropout2 = dropout
        if self.dropout is not None:
            self.dropout1 = nn.Dropout(dropout1)
        self.pre_classifier_fc = nn.Linear(embed_dim, embed_dim)
        if self.dropout is not None:
            self.dropout2 = nn.Dropout(dropout2)
        self.classifier = nn.Linear(embed_dim, 1)

    def forward(self, embedded):
        if self.dropout1 is not None:
            embedded = self.dropout1(embedded)
        embedded = self.pre_classifier_fc(embedded)
        if self.dropout2 is not None:
            embedded = self.dropout2(embedded)
        return torch.sigmoid(self.classifier(embedded))