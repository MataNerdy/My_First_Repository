import math

import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

torch.manual_seed(42)


class SinCosDataset(Dataset):
    def __init__(self, num_points: int=512):
        x = torch.linspace(-2*math.pi, 2*math.pi, num_points)
        self.x = x.unsqueeze(1)
        self.y = 0.25 + torch.sin(self.x) + 0.35 * torch.cos(2 * self.x)

    def __len__(self) -> int:
        return len(self.x)

    def __getitem__(self, index: int):
        return self.x[index], self.y[index]

train_dataset = SinCosDataset(num_points=512)
print(len(train_dataset))
x_example, y_example = train_dataset[0]
print(tuple(x_example.shape), tuple(y_example.shape))

train_loader = DataLoader(dataset=train_dataset, batch_size=64, shuffle=True)

x_batch, y_batch = next(iter(train_loader))
print(tuple(x_batch.shape), tuple(y_batch.shape))

class SmallRegressor(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(1, 32),
            nn.SiLU(),
            nn.Linear(32, 32),
            nn.SiLU(),
            nn.Linear(32, 1)
        )
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.network(x)

model = SmallRegressor()

test_output = model(torch.zeros(8, 1))
print(model)
print(test_output.shape)
print(sum(p.numel() for p in model.parameters()))

loss_fn = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)

print(loss_fn)
print(optimizer)

num_epoch = 200
loss_history = []

model.train()

for epoch in range(num_epoch):
    epoch_loss = 0.0
    for x_batch, y_batch in train_loader:
        optimizer.zero_grad()
        pred = model(x_batch)
        loss = loss_fn(pred, y_batch)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item() * x_batch.size(0)
    epoch_loss += epoch_loss / len(train_dataset)
    loss_history.append(epoch_loss)
    if (epoch + 1) % 20 == 0:
        print(f"Эпоxa {epoch + 1 :> 3}, MSE: {epoch_loss:.6f}")

model.eval()

with torch.no_grad():
    x_plot = torch.linspace(-2*math.pi, 2*math.pi, 500)
    x_plot = x_plot.unsqueeze(1)
    y_true = 0.25 + torch.sin(x_plot) + 0.35 * torch.cos(2 * x_plot)
    y_pred = model(x_plot)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].plot(loss_history)
axes[0].set_yscale('log')
axes[0].set_title('Ошибка во время обучения')
axes[0].set_xlabel('эпоха')
axes[0].set_ylabel('MSE, логарифмическая шкала')
axes[0].grid(alpha=0.25)

axes[1].plot(x_plot.squeeze(), y_true.squeeze(), color='black', linewidth=2, label='правильная функция')
axes[1].plot(x_plot.squeeze(), y_pred.squeeze(), color='tab:blue', label='нейросеть')
axes[1].set_title('Предсказание модели')
axes[1].set_xlabel('x')
axes[1].set_ylabel('y')
axes[1].grid(alpha=0.25)
axes[1].legend()

plt.tight_layout()
plt.show()

final_mse = loss_fn(y_pred, y_true).item()
print(final_mse)
if final_mse < 0.01:
    print('Отлично: модель выучила форму функции!')
else:
    print('Модель пока ошибается. Проверьте training loop или попробуйте обучать дольше.')
