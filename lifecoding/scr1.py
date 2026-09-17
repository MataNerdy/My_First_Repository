import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

class LinReg(nn.Module):
    def __init__(self, input, output):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input, 128),
            nn.SiLU(),
            nn.Linear(128, 128),
            nn.SiLU(),
            nn.Linear(128, output)
        )

    def forward(self, x):
        return self.model(x)

x = torch.linspace(-10, 10, 1000).reshape(-1, 1)
y = x ** 2
print(x.shape, y.shape)

model = LinReg(1, 1)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.0001)
model.train()

for i in range(2000):
    pred = model(x)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    print(f"epoch={i+1}, loss={loss.item()}")

with torch.no_grad():
    plt.figure(figsize=(10,8))
    plt.plot(x.numpy(), y.numpy(), c='r')
    plt.plot(x.numpy(), pred.numpy(), c='b')
    plt.show()
