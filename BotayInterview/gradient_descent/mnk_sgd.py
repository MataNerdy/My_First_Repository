import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import LinearRegression

N, p = 1000000, 100
X = np.random.randn(N,p)
y = X @ np.random.randn(p) + np.random.randn(N) * 0.1

model_mnk = LinearRegression().fit(X, y)

model_sgd = SGDRegressor(max_iter=10, tol=1e-3)
model_sgd.fit(X, y)
