import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
N, d = 100, 1
X = np.random.randn(N, d)
y = (2 * X.squeeze() + 1 + 0.1 * np.random.randn(N))

X_b = np.column_stack([np.ones(N), X])

w_ols = np.linalg.inv(X_b.T @ X_b) @ X_b.T @ y
print("OLS weights:", w_ols)

w_gd = np.zeros(2)
lr = 0.1
losses = []

for i in range(200):
    y_pred = X_b @ w_gd
    loss = np.mean((y_pred - y)**2)
    losses.append(loss)
    grad = (X_b.T @ (y_pred - y)) / N
    w_gd -= lr * grad

print("GD weights:", w_gd)
plt.plot(losses)
plt.title("Сходимость градиентного спуска")
plt.xlabel("Iteration")
plt.ylabel("MSE")
plt.grid()
plt.show()

print("Difference:", np.abs(w_ols-w_gd))
