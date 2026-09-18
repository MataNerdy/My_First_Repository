import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset

class CustomDataset(Dataset):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, index):
        return self.x[index], self.y[index]

class MLP(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.ln1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.ln2 = nn.Linear(hidden_size, output_size)
    def forward(self, x):
        x = self.ln1(x)
        x = self.relu(x)
        x = self.ln2(x)
        return x

X = torch.randn(1000, 20)
y = torch.randint(0, 5, (1000,))

dataset = CustomDataset(X, y)
loader = DataLoader(dataset, batch_size=32)

model = MLP(input_size=20, hidden_size=64, output_size=5)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

model.train()
for epoch in range(100):
    losses = []
    for x, y in loader:
        optimizer.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        losses.append(loss.item())

    print(f'epoch: {epoch}: {sum(losses)/len(losses)}')

model.eval()
with torch.no_grad():
    correct = 0
    total = 0
    for x, y in loader:
        logits = model(x)
        labels = torch.argmax(logits, dim=1)
        correct += (labels == y).sum().item()
        total += y.size(0)
    print(correct/total)
