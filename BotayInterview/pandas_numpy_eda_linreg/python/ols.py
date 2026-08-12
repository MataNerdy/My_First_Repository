import numpy as np
from sklearn.linear_model import LinearRegression

X = np.array([[1, 2], [2, 4], [4, 9], [9, 16]], dtype=float)
y = np.array([3, 5, 7, 9], dtype=float)
# Добавляем столбец единиц для смещения
X = np.column_stack([np.ones(X.shape[0]), X])
print(X)
# Решение
w = np.linalg.inv(X.T @ X) @ X.T @ y
print("Веса МНК:", w)

model = LinearRegression(fit_intercept=False)
model.fit(X, y)
print("Веса Sklearn:", model.coef_)