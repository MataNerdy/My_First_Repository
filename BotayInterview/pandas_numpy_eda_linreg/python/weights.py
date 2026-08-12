import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[1,2], [2,4], [4,9], [9,16]], dtype=float)
y = np.array([3, 5, 7, 9], dtype=float)

X_with_bias = np.column_stack([np.ones(X.shape[0]), X])

model = LinearRegression(fit_intercept=False)
model.fit(X_with_bias, y)
w_lr = model.coef_
print("Веса LR:", w_lr)

XTX_inv = np.linalg.inv(X_with_bias.T @ X_with_bias)
w_ols = XTX_inv @ X_with_bias.T @ y
print("Веса МНК:", w_ols)

w = np.random.randn(X_with_bias.shape[1])
lr = 0.01

for e in range(1000):
    y_pred = X_with_bias @ w
    grad = (X_with_bias.T @ (y_pred - y)) / len(y)
    w -= grad * lr
    if e % 100 == 0:
        loss = np.mean((y_pred - y)**2)
        print(f"Epoch {e}: {loss:.4f}")
print("Веса GD:", w)
