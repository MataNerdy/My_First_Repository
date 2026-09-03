import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
import torch
from torch import nn

X_n, y_n = datasets.make_regression(n_samples=100, n_features=1, noise=20, random_state=1)

X = torch.from_numpy(X_n.astype(np.float32))
y = torch.from_numpy(y_n.astype(np.float32))

y = y.view(y.shape[0], 1)

n_samples, n_features = X.shape

input_size = n_features
output_size = 1
model = nn.Linear(input_size, output_size)

criterion = nn.MSELoss()
learning_rate = 0.01
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

num_epochs = 100
for epoch in range(num_epochs):
    pred = model(X)
    loss = criterion(pred, y)
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    if epoch % 10 == 0:
        print(f"epoch: {epoch+1}, loss = {loss.item():.4f}")

predicted = model(X).detach().numpy()
plt.plot(X_n, y_n, 'ro')
plt.plot(X_n, predicted, 'b')
plt.show()
