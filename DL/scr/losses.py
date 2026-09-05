import torch
import torch.nn as nn
import torch.nn.functional as F


torch.manual_seed(42)
torch.set_printoptions(precision=3, sci_mode=False)

binary_logits = torch.tensor([-2.0, 0.0, 2.0])
binary_probabilities = torch.sigmoid(binary_logits)
binary_target = torch.tensor([0.0, 1.0, 1.0])

bce = nn.BCEWithLogitsLoss(reduction='none')
losses = bce(binary_logits, binary_target)

print(f"{binary_logits=}")
print(f"{binary_probabilities=}")
print(f"{binary_target=}")
print(f"{losses=}")
print(f"Mean: {losses.mean()}")

multiclass_logits = torch.tensor([
    [3.0, 1.0, -1.0],
    [0.2, 2.0, 0.1],
    [-1.0, 0.0, 2.0]
])

class_targets = torch.tensor([0, 1, 2])
cross_entropy = nn.CrossEntropyLoss(reduction='none')
ce_losses = cross_entropy(multiclass_logits, class_targets)

print(f'After softmax {torch.softmax(multiclass_logits, dim=1)}')
print(f"{class_targets=}")
print(f"{ce_losses=}")
print(f"Mean: {ce_losses.mean()}")

binary_model_output = torch.randn(5)
binary_target = torch.tensor([0.0, 1.0, 1.0, 0.0, 1.0])

print("BCE output", tuple(binary_model_output.shape))
print("BCE target", tuple(binary_target.shape), binary_target.dtype)

multiclass_model_output = torch.randn(5, 3)
multiclass_target = torch.tensor([0, 2, 1, 0, 2])

print("CE output", tuple(multiclass_model_output.shape))
print("CE target", tuple(multiclass_target.shape), multiclass_logits.dtype)

focal_logits = torch.tensor([
    [4.0, 0.0],
    [0.2, 0.0],
    [0.0, 4.0]
])

focal_targets = torch.tensor([0, 0, 0])

ce_each = F.cross_entropy(focal_logits, focal_targets, reduction='none')
true_class_probabilities = torch.softmax(focal_logits, dim=1).gather(
    dim=1,
    index=focal_targets[:, None],
).squeeze(1)

gamma = 2.0
focal_weight = (1 - true_class_probabilities).pow(gamma)
focal_each = focal_weight * ce_each

names = ['easy', 'unconfidence', 'mistake']
for n, p, ce, w, fv in zip(
    names,
    true_class_probabilities,
    ce_each,
    focal_weight,
    focal_each
):
    print(f"name: {n:11s} | p right class: {p:.3f}")
    print(f"| CE: {ce:.3f} | weight: {w:.3f} | focal value: {fv:.3f}")

def focal_cross_entropy(
        logits: torch.Tensor,
        targets: torch.Tensor,
        gamma: float=2.0
) -> torch.Tensor:
    if gamma < 0:
        raise ValueError('gamma должна быть неотрицательной')

    ce = F.cross_entropy(logits, targets, reduction='none')
    true_class_prob = torch.exp(-ce)
    focal_weight = (1.0 - true_class_prob).pow(gamma)
    return(focal_weight * ce).mean()

ordinary_ce = F.cross_entropy(focal_logits, focal_targets)
focal_gamma_0 = focal_cross_entropy(focal_logits, focal_targets, gamma=0)
focal_gamma_2 = focal_cross_entropy(focal_logits, focal_targets, gamma=2)

print(ordinary_ce)
print(focal_gamma_0)
print(focal_gamma_2)


features = torch.tensor([
    [-2.0, -1.0],
    [-1.0, -2.0],
    [1.0, 2.0],
    [2.0, 1.0],
])

targets = torch.tensor([0,0,1,1])

model = nn.Linear(2, 2)
optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
criterion = nn.CrossEntropyLoss()

optimizer.zero_grad()
logits = model(features)
loss = criterion(logits, targets)
loss.backward()
optimizer.step()

print(logits.shape)
print(loss.item())
print(model.weight.grad is not None)

def focal_cross_entropy_alpha_debug(
        logits: torch.Tensor,
        targets: torch.Tensor,
        alpha: torch.Tensor,
        gamma: float=2.0
):
    if gamma < 0:
        raise ValueError('gamma должна быть неотрицательной')

    ce = F.cross_entropy(logits, targets, reduction='none')
    true_class_prob = torch.exp(-ce)
    focal_weight = (1.0 - true_class_prob).pow(gamma)
    each_alpha = alpha[targets]
    loss_each = each_alpha * focal_weight * ce
    loss = loss_each.mean()
    print(f'All classes probabilities: {torch.softmax(logits, dim=1)}')
    print(f'CE: {ce}')
    print(f'True class probability: {true_class_prob}')
    print(f'Focal-weight: {focal_weight}')
    print(f'Alpha: {each_alpha}')
    print(f'Loss: {loss_each}')
    print(f'Mean loss: {loss}')
    return loss


logits = torch.tensor([
    [3.0, 1.0, 0.0],
    [0.0, 1.0, 0.0],
    [3.0, 1.0, 0.0]
])

targets = torch.tensor([0, 1, 2])
alpha = torch.tensor([0.2, 0.5, 1.0])

loss2 = focal_cross_entropy_alpha_debug(
    logits=logits,
    targets=targets,
    alpha=alpha,
    gamma=2.0
)

print(loss2)

loss0 = focal_cross_entropy_alpha_debug(
    logits=logits,
    targets=targets,
    alpha=alpha,
    gamma=0
)

weighted_ce = (alpha[targets] * F.cross_entropy(logits, targets, reduction='none')).mean()
print(loss0, 'vs', weighted_ce)
assert torch.allclose(loss0, weighted_ce)
print("Тест пройден!")