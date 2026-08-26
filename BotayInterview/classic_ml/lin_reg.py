import numpy as np

X = np.array([[1,2], [2,3], [3,4], [4,6]], dtype=float)
y = np.array([3, 5, 7, 9], dtype=float)

X_with_bias = np.column_stack([np.ones(X.shape[0]), X])

XTX_inv = np.linalg.inv(X_with_bias.T @ X_with_bias)
w_ols = XTX_inv @ X_with_bias.T @ y
print(w_ols)

w = np.random.randn(X_with_bias.shape[1])
lr = 0.01
for epoch in range(10000):
    y_pred = X_with_bias @ w
    grad =  (X_with_bias.T @ (y_pred - y)) / len(y)
    w -= lr * grad
    if epoch % 200 == 0:
        loss = np.mean((y_pred - y) ** 2)
        print(f"Эпоха {epoch}, лосс: {loss:.4f}")

print(w)
