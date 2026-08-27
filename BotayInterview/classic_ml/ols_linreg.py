import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[1,2], [2,3], [3,4], [4,6]], dtype=float)
y = np.array([3, 5, 7, 9], dtype=float)

X = np.column_stack([np.ones(X.shape[0]), X])

XTX_inv = np.linalg.inv(X.T @ X)
w_ols = XTX_inv @ X.T @ y
print(w_ols)

model = LinearRegression(fit_intercept=False)
model.fit(X, y)
print(model.coef_)