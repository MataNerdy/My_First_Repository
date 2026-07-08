import torch
import torch.nn as nn

model = nn.Sequential(nn.Linear(10, 100),
                      nn.ReLU(),
                      nn.Linear(100,1))
criterion = nn.MSELoss()
optimizer = torch.optim.SGD(model.parameters(), lr=5)

x = torch.randn(32, 10)
y = torch.randn(32, 1)

loss = criterion(model(x), y)
print("Loss до backpropagation:", loss.item())

loss.backward()
optimizer.step()

try:
    new_loss = criterion(model(x), y)
    print("Loss после backpropagation:", new_loss.item())
except:
    print("Loss стал NaN или inf")