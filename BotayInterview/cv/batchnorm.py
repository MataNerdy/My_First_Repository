from torch import nn

bn = nn.BatchNorm2d(128)
print(sum(p.numel() for p in bn.parameters()))

print(bn.weight.shape)
print(bn.bias.shape)