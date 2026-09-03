import torch

x = torch.rand(3, requires_grad=True)
print(x)
y = x + 2
print(y)
z = y*y*2
z = z.mean()
print(z)

v = torch.tensor([1, 1, 1], dtype=torch.float32)/3
z.backward()
print(x.grad)
with torch.no_grad():
    y = 4*(x+2)/3
    print(y)
    print(x)

weights = torch.ones(4, requires_grad=True)

for epoch in range(3):
    model_output = (weights*3).sum()
    model_output.backward()
    print(weights.grad)
    weights.grad.zero_()
