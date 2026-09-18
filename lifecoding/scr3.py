import torch
import torch.nn as nn
import torch.optim as optim

x = torch.randn(200, 10)
y = torch.randint(0, 4, (200,))

class LinModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(10, 4)

    def forward(self, x):
        return self.linear(x)

model = LinModel()
pred = model(x)
print(x.shape, y.shape, pred.shape)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters())

model.train()
for epoch in range(100):
    optimizer.zero_grad()
    pred = model(x)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()
    print(f"{epoch}: loss={loss.item()}")

model.eval()
with torch.no_grad():
    pred = model(x)
    labels = torch.argmax(pred, dim=1)
    acc = (y == labels).float().mean()
    print(acc)
