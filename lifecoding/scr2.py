import torch
import torch.nn as nn
import torch.optim as optim


x = torch.randn(100, 10)
y = torch.randint(0, 2, (100,)).float().reshape(-1, 1)

class LinModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 1)
        self.sigmoid = nn.Sigmoid()
    def forward(self, x):
        return self.sigmoid(self.linear(x))

model = LinModel()
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters())
pred = model(x)
print(pred.shape)
model.train()
for epoch in range(100):
    optimizer.zero_grad()
    pred = model(x)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()
    print(f"{epoch=} loss: {loss.item()}")

model.eval()
with torch.no_grad():
    pred = model(x)
    acc = ((pred > 0.5).float() == y).float().mean()
    print(acc)
