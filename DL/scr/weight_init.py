import math

import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt


torch.manual_seed(42)

x = torch.linspace(-2 * math.pi, 2 * math.pi, 256).unsqueeze(1)
y = 0.25 + torch.sin(x) + 0.34 * torch.cos(2 * x)

plt.figure(figsize=(8, 3.5))
plt.plot(x.squeeze(), y.squeeze(), color='black', linewidth=2)
plt.title(r'Data: $0.25 + \sin(x) + 0.35\cos(2x)$')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(alpha=0.25)
plt.show()

class SmallRegressor(nn.Module):
    def __init__(self, hidden_dim: int=32):
        super().__init__()
        self.fc1 = nn.Linear(1, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.out = nn.Linear(hidden_dim, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = F.silu(self.fc1(x))
        x = F.silu(self.fc2(x))
        return self.out(x)

def initialize_with_zeros(model: nn.Module) -> None:
    if isinstance(model, nn.Linear):
        nn.init.zeros_(model.weight)
        nn.init.zeros_(model.bias)

default_model = SmallRegressor()

zero_model = SmallRegressor()
zero_model.apply(initialize_with_zeros)

print(f'First 5 weights default model: {default_model.fc1.weight[:5, 0].detach()}')
print(f'First 5 weights zero model: {zero_model.fc1.weight[:5, 0].detach()}')

print(f'PyTorch: {torch.__version__}')

for name, layer in [
                    ('fc1', default_model.fc1),
                    ('fc2', default_model.fc2),
                    ('out', default_model.out)]:
    fan_in = layer.in_features
    bound = 1 / math.sqrt(fan_in)
    weights = layer.weight.detach()
    print(
        f'{name:>3}: {fan_in=:>2}, '
        f'ожидаемый диапазон=[{-bound:.4f}, {bound:.4f}], '
        f'фактический=[{weights.min():.4f}, {weights.max():.4f}]'
    )

fig, axes = plt.subplots(1, 2, figsize=(10, 3.5), sharey=True)
axes[0].hist(default_model.fc2.weight.detach().flatten(), bins=20, color='tab:blue')
axes[0].set_title('Стандартная инициализация')
axes[1].hist(zero_model.fc2.weight.detach().flatten(), bins=20, color='tab:red')
axes[1].set_title('Нулевая инициализация')
for ax in axes:
    ax.set_xlabel('значение веса')
    ax.set_ylabel('количество')
    ax.grid(alpha=0.2)
plt.tight_layout()
plt.show()

def train(model: nn.Module, steps: int=1200, lr: float=1e-2):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    history = []
    for step in range(steps):
        prediction = model(x)
        loss = F.mse_loss(prediction, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if step % 10 == 0:
            history.append((step, loss.item()))
    return history

default_history = train(default_model)
zero_history = train(zero_model)

default_model.eval()
zero_model.eval()

with torch.no_grad():
    default_pred = default_model(x)
    zero_pred = zero_model(x)

print(f'Финальный MSE, стандартная инициализация: {F.mse_loss(default_pred, y).item():.6f}')
print(f'Финальный MSE, нулевая инициализация: {F.mse_loss(zero_pred, y).item():.6f}')

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

for history, label, color in [
        (default_history, 'стандартная', 'tab:red'),
        (zero_history, 'нулевая', 'tab:blue'),
        ]:
    steps, losses = zip(*history)
    axes[0].plot(steps, losses, label=label, color=color)

axes[0].set_yscale('log')
axes[0].set_title('Ошибка во время обучения')
axes[0].set_xlabel('шаг')
axes[0].set_ylabel('MSE, логарифмическая шкала')
axes[0].grid(alpha=0.25)
axes[0].legend()

axes[1].plot(x.squeeze(), y.squeeze(), color='black', linewidth=2, label='целевая функция')
axes[1].plot(x.squeeze(), default_pred.squeeze(), color='tab:blue', label='стандартная')
axes[1].plot(x.squeeze(), zero_pred.squeeze(), color='tab:red', linestyle='--', label='нулевая')
axes[1].set_title('Результат после обучения')
axes[1].set_xlabel('x')
axes[1].set_ylabel('y')
axes[1].grid(alpha=0.25)
axes[1].legend()

plt.tight_layout()
plt.show()

print('Максимальный модуль веса fc1 нулевой модели:')
print(zero_model.fc1.weight.detach().abs().max().item())
print('Выходной bias нулевой модели и среднее целевой функции:')
print('bias =', zero_model.out.bias.detach().item())
print('mean(y)=', y.mean().item())