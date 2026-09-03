import torch

x = torch.tensor(0.4)
y = torch.tensor(2.0)
w = torch.tensor(2.5, requires_grad = True)
y_hat = x * w
loss = (y_hat - y)**2

print(loss)

loss.backward()
print(w.grad)
