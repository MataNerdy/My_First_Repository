import torch
import torch.nn.functional as F

y_true = torch.tensor([0., 1., 1., 0., 0.])
y_pred = torch.tensor([0.2, 0.9, 0.8, 0.3, 0.1])

pos_weight = torch.tensor([3.0])
loss = F.binary_cross_entropy_with_logits(
    torch.logit(y_pred), y_true, pos_weight=pos_weight
)
print("Weighted loss:", loss.item())