import torch
import torch.nn as nn


torch.set_printoptions(precision=3, sci_mode=False)

def count_trainable_parameters(module: nn.Module) -> int:
    return sum(p.numel() for p in module.parameters() if p.requires_grad)

trainable_layer_norm = nn.LayerNorm(2)

tokens = torch.tensor([
    [1.0, 3.0],
    [101.0, 103.0]
])

layer_norm_without_parameters = nn.LayerNorm(
    normalized_shape=2,
    elementwise_affine=False
)

layer_norm_result = layer_norm_without_parameters(tokens)

print(tokens)

for n, p in trainable_layer_norm.named_parameters():
    print(f'{n:6s}: {p.tolist()} - {p.numel()} params')

print('Всего обучаемых параметров:', count_trainable_parameters(trainable_layer_norm))

for n, p in layer_norm_without_parameters.named_parameters():
    print(f'{n:6s}: {p.tolist()} - {p.numel()} params')

print('Всего обучаемых параметров:', count_trainable_parameters(layer_norm_without_parameters))

batch_norm = nn.BatchNorm1d(
    num_features=2,
    affine=False,
    track_running_stats=False
)

batch_norm_result = batch_norm(tokens)

print(tokens)
print(f'{layer_norm_result=}')
print(layer_norm_result.mean(dim=1))
print(f'{batch_norm_result=}')
print(batch_norm_result.mean(dim=0))

first_token = torch.tensor([[1.0, 3.0]])
batch_a = torch.tensor([
    [1.0, 3.0],
    [5.0,   7.0],
    [101.0, 103.0],
])
batch_b = torch.tensor([
    [1.0, 3.0],
    [2.0, 4.0],
    [5.0, 7.0],
])

simple_batch_norm = nn.BatchNorm1d(
    num_features=2,
    affine=False,
    track_running_stats=False
)

first_batch_a = simple_batch_norm(batch_a)
first_batch_b = simple_batch_norm(batch_b)

print('Первый токен в batch A:', first_batch_a)
print('Первый токен в batch B:', first_batch_b)
print('Результаты отличаются, хотя сам первый токен не менялся.')

class RMSNorm(nn.Module):
    def __init__(
            self,
            normalized_shape:int,
            eps: float=1e-8,
            elementwise_affine: bool=True
    ):
        super().__init__()
        self.eps = eps
        if elementwise_affine:
            self.weight = nn.Parameter(torch.ones(normalized_shape))
        else:
            self.register_parameter('weight', None)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        mean_square = x.pow(2).mean(dim=-1, keepdim=True)
        normalized = x * torch.rsqrt(mean_square + self.eps)

        if self.weight is not None:
            normalized = normalized * self.weight
        return normalized


rms_norm = RMSNorm(2, elementwise_affine=False)
rms_norm_result = rms_norm(tokens)

print('После LayerNorm:', layer_norm_result)
print('После RMSNorm:', rms_norm_result)
print('Среднее строк после RMSNorm не обязано быть нулём:', rms_norm_result.mean(dim=1))

tokens_4_f = torch.tensor([
    [1.0, 3.0, 10.0, 14.0],
    [101.0, 103.0, 210.0, 214.0]
])

print(tokens.shape)

group_norm = nn.GroupNorm(
    num_groups=2,
    num_channels=4,
    affine=False
)

print('До GroupNorm:', tokens_4_f)
print('После GroupNorm:', group_norm(tokens_4_f))

signals = torch.tensor([
    [
        [1.0, 2.0, 3.0],
        [10.0, 20.0, 30.0],
    ],
    [
        [101.0, 102.0, 103.0],
        [1000.0, 2000.0, 3000.0],
    ]
])

instance_norm = nn.InstanceNorm1d(
    num_features=2,
    affine=False,
    track_running_stats=False
)

print('До InstanceNorm1d:', signals, signals.shape)
print('После InstanceNorm1d:', instance_norm(signals))

small_perceptron = nn.Sequential(
    nn.Linear(2, 4),
    nn.LayerNorm(4),
    nn.ReLU(),
    nn.Linear(4, 1)
)

prediction = small_perceptron(tokens)

print(small_perceptron)
print("Input", tokens.shape)
print('Ouput', prediction.shape)
print('Params:', count_trainable_parameters(small_perceptron))
print('LayerNorm params:', count_trainable_parameters(small_perceptron[1]))