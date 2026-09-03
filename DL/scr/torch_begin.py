import numpy as np
import torch

x = np.ones(5)
print(x)
a = torch.from_numpy(x)
print(a)
b = torch.tensor(x, dtype=torch.float32)
print(b)

x += 1
print(x)
print(a)
print(b)

if torch.cuda.is_available():
    device = torch.device("cuda")
    c = torch.zeros(5, device=device)
    d = torch.ones(5)
    d = d.to(device)
    e = d + c
    e = e.to('cpu')
    print(c)
    print(d)
    print(e)