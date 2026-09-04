import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt


torch.manual_seed(42)

def relu(x):
    if x < 0:
        return 0
    return x

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

class SwiGLU(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int):
        super().__init__()
        self.gate_proj = nn.Linear(input_dim, hidden_dim)
        self.value_proj = nn.Linear(input_dim, hidden_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        gate = F.silu(self.gate_proj(x))
        value = self.value_proj(x)
        return gate * value

batch = torch.randn(4, 8)
layer = SwiGLU(input_dim=8, hidden_dim=16)
output = layer(batch)

print('Вход: ', tuple(batch.shape))
print('Выход:', tuple(output.shape))
print('Обучаемых параметров:', sum(p.numel() for p in layer.parameters()))

x = torch.linspace(-5, 5, 500)
relu_y = F.relu(x)
silu_y = F.silu(x)

swiglu_toy_y = F.silu(x)*x
fig, axes = plt.subplots(1, 2, figsize=(11, 4))

axes[0].plot(x, relu_y, label='ReLU', linewidth=2)
axes[0].plot(x, silu_y, label='SiLU', linewidth=2)
axes[0].axhline(0, color='black', linewidth=0.6)
axes[0].axvline(0, color='black', linewidth=0.6)
axes[0].set_title('Поэлементные активации')
axes[0].grid(alpha=0.25)
axes[0].legend()

axes[1].plot(x, swiglu_toy_y, color='tab:green', label=r'$x \cdot SiLU(x)$', linewidth=2)
axes[1].axhline(0, color='black', linewidth=0.6)
axes[1].axvline(0, color='black', linewidth=0.6)
axes[1].set_title('Поэлементные активации')
axes[1].grid(alpha=0.25)
axes[1].legend()

for ax in axes:
    ax.set_xlabel('x')
    ax.set_ylabel('выход')

plt.tight_layout()
plt.show()