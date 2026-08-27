import numpy as np
from sklearn.linear_model import LinearRegression, SGDRegressor

N, p = 1000000, 100
X = np.random.randn(N, p)
y = X @ np.random.randn(p) + 0.1 * np.random.randn(N)

model_mnk = LinearRegression().fit(X, y)
model_sgd = SGDRegressor(max_iter=10, tol=1e-3)
model_sgd.fit(X, y)