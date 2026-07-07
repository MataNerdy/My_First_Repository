import torch
import torch.nn as nn

model = nn.TransformerEncoderLayer(
        nn.TransformerEncoderLayer(
        d_model=128, nhead=4,
        batch_first=True),
        num_layers=2)

optimizer_1 = torch.optim.Adam(model.parameters(), lr=1e-3)
optimizer_2 = torch.optim.AdamW(model.parameters(), lr=2.5e-5, weight_decay=0.01)
optimizer_3 = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9)