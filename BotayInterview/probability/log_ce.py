import torch
import torch.nn.functional as F
from torch import nn

torch.manual_seed(42)
N=1000
X = torch.ones(N, 10)
y = torch.bernoulli(torch.full((N,), 0.3)).float()

model = nn.Linear(10, 1)
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)

print("Initial Loss")
with torch.no_grad():
    logits = model(X)
    p = torch.sigmoid(logits)
    loss = F.binary_cross_entropy(p.squeeze(), y)
    print(f"Средняя предсказанная вероятность: {p.mean().item():.4f}")
    print(f"Эмпирическая частота метки 1: {y.mean().item():.4f}")
    print(f"Лосс: {loss.item():.4f}")

optimizer.zero_grad()
logits = model(X)
p = torch.sigmoid(logits)
loss = F.binary_cross_entropy(p.squeeze(), y)
loss.backward()
optimizer.step()
print("After one step")
with torch.no_grad():
    p = torch.sigmoid(model(X))
    print(f"Средняя предсказанная вероятность: {p.mean().item():.4f}")
    print("Модель начинает тянуть предсказания к эмпирической частоте — именно потому, что кросс-энтропия оптимизирует правдоподобие!")
