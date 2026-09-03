import numpy as np
import torch
from torch import nn


def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def cross_enthropy(y, y_pred):
    loss = np.sum(-y * np.log(y_pred))
    return loss

x = np.array([2.0, 1.0, 0.1])
outputs = softmax(x)

print("Softmax numpy:", outputs)

x = torch.tensor([2.0, 1.0, 0.1])
outputs = torch.softmax(x, dim=0)

print("Softmax torch:", outputs)

Y = np.array([1, 0, 0])
Y_pred_good = np.array([0.7, 0.2, 0.1])
Y_pred_bad = np.array([0.1, 0.3, 0.6])
l1 = cross_enthropy(Y, Y_pred_good)
l2 = cross_enthropy(Y, Y_pred_bad)
print("Cross-entropy (good):", l1)
print("Cross-entropy (bad):", l2)

loss = nn.CrossEntropyLoss()
Y = torch.tensor([2, 0, 1])
Y_pred_good = torch.tensor([[0.1, 1.0, 2.1], [2.0, 1.0, 0.1], [0.1, 3.0, 0.1]])
Y_pred_bad = torch.tensor([[2.1, 1.0, 0.1], [0.1, 1.0, 2.1], [0.1, 3.0, 0.1]])

l1 = loss(Y_pred_good, Y)
l2 = loss(Y_pred_bad, Y)

print(l1.item())
print(l2.item())

_, predictions1 = torch.max(Y_pred_good, 1)
_, predictions2 = torch.max(Y_pred_bad, 1)

print(predictions1)
print(predictions2)