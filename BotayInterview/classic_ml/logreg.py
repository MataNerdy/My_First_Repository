import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=200,
    n_features=2,
    n_redundant=0,
    n_informative=2,
    n_clusters_per_class=1,
    class_sep=2.0,
    random_state=42
)

model = LogisticRegression()
model.fit(X, y)

w1, w2 = model.coef_[0]
b = model.intercept_[0]

x1_vals = np.linspace(X[:,0].min() - 1, X[:,0].max() + 1, 100)
x2_vals = -(w1 * x1_vals + b) / w2

plt.scatter(X[y == 0, 0], X[y == 0, 1], label='Class 0', alpha=0.7)
plt.scatter(X[y == 1, 0], X[y == 1, 1], label='Class 1', alpha=0.7)
plt.plot(x1_vals, x2_vals, 'k--', label="Linear bound")
plt.title('Логистическая регрессия: линейный классификатор')
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.legend()
plt.grid(True)
plt.show()

print(f"Уравнение границы: {w1:.2f}·x₁ + {w2:.2f}·x₂ + {b:.2f} = 0")
print("Граница — прямая линия → модель линейна.")