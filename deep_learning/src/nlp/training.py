import torch

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import display, HTML
from tqdm.notebook import tqdm

# For binary accuracy, we can define a function or use a library like torchmetrics
def binary_accuracy(preds, y):
    # Round predictions to the closest integer (0 or 1)
    rounded_preds = torch.round(preds)
    correct = (rounded_preds == y).float()  # Convert into float for division
    acc = correct.sum() / len(correct)
    return acc

class TextClassificationTrainer:
    def __init__(self, model, loss_function, hyper_params, device='cuda', metric_fn=None):
        self.model = model.to(device)
        self.device = device
        self.loss_function = loss_function
        learning_rate = hyper_params.get('learning_rate', 1e-3)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate)
        self.train_history = []
        self.metric_fn = metric_fn if metric_fn is not None else binary_accuracy

    def train(self, train_loader, val_loader, num_epochs):
        current_epoch = max([0] + [x['epoch'] for x in self.train_history])
        max_epochs = current_epoch + num_epochs
        for epoch in range(current_epoch, current_epoch + num_epochs):
            # Training phase
            self.model.train()
            train_progress_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{max_epochs} [Training]")  # Wrap train_loader with tqdm
            for texts, labels in train_progress_bar:
                texts, labels = texts.to(self.device), labels.to(self.device)
                self.optimizer.zero_grad()
                predictions = self.model(texts).squeeze(1)

                loss = self.loss_function(predictions, labels)
                acc = self.metric_fn(predictions, labels)
                loss.backward()
                self.optimizer.step()

                self.train_history.append({
                    'epoch': epoch,
                    'split': 'train',
                    'loss': loss.item(),
                    'acc': acc.item()
                })
        
            epoch_train_stats = pd.DataFrame(self.train_history).query(f"epoch == {epoch} and split == 'train'")
            loss = epoch_train_stats['loss'].mean()
            acc = epoch_train_stats['acc'].mean()
            print (f"Epoch {epoch} train loss: {loss:.4f}, acc: {acc:.4f}")

            self.validate(val_loader, 'dev')

    def validate(self, data_loader, split, save_in_history=True):
        epoch = max([0] + [x['epoch'] for x in self.train_history])
        self.model.eval()
        results = []
        losses, accs = [], []
        with torch.no_grad():
            for texts, labels in data_loader:
                texts, labels = texts.to(self.device), labels.to(self.device)
                predictions = self.model(texts).squeeze(1)
                loss = self.loss_function(predictions, labels)
                acc = self.metric_fn(predictions, labels)

                for i in range(len(predictions)):
                    token_ids = texts[i].cpu().numpy()
                    results.append({
                        'token_ids': token_ids,
                        'label': labels[i].item(),
                        'prediction': predictions[i].item()
                    })
                losses.append(loss.item())
                accs.append(acc.item())
                
                if save_in_history:
                    self.train_history.append({
                        'epoch': epoch,
                        'split': split,
                        'loss': loss.item(),
                        'acc': acc.item()
                    })
            
            loss = sum(losses) / len(losses)
            acc = sum(accs) / len(accs)
            print (f"Epoch {epoch} {split} loss: {loss:.4f}, acc: {acc:.4f}")
        return results

    def plot_history(self):
        # see plot of training and validation loss
        history_df = pd.DataFrame(self.train_history).groupby(['epoch', 'split']).mean().reset_index()
        plt.figure(figsize=(14, 6))
        plt.subplot(1, 2, 1)
        sns.lineplot(x='epoch', y='loss', hue='split', data=history_df)
        plt.title("Loss")
        plt.subplot(1, 2, 2)
        sns.lineplot(x='epoch', y='acc', hue='split', data=history_df)
        plt.title("Accuracy")
        plt.show()

    

