import torch
import torch.nn as nn
import torch.optim as optim

x = torch.randn(100, 5)
y = torch.randint(0, 3, (100,))

class LinModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Linear(5, 16)
        self.relu = nn.ReLU()
        self.l2 = nn.Linear(16, 3)
    def forward(self, x):
        return self.l2(self.relu(self.l1(x)))

model = LinModel()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

model.train()
for epoch in range(100):
    optimizer.zero_grad()
    pred = model(x)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()

    print(f'{epoch=} loss={loss.item()}')

model.eval()
with torch.no_grad():
    logits = model(x)
    labels = torch.argmax(logits, dim=1)
    acc = (y == labels).float().mean()
    print(acc)