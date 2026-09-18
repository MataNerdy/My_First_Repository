import torch
import torch.nn as nn
import torch.optim as optim

x = torch.randn(100, 5)
y = torch.randint(0, 3, (100,))

W = torch.randn(5, 3, requires_grad=True)
b = torch.zeros(3, requires_grad=True)


optimizer = optim.Adam([W,b])
criterion = nn.CrossEntropyLoss()

for epoch in range(100):
    optimizer.zero_grad()
    pred = x @ W + b
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()

with torch.no_grad():
    pred = x @ W + b
    labels = torch.argmax(pred, dim=1)
    acc = (y == labels).float().mean()

print(acc)
