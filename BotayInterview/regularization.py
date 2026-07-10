import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Lasso, Ridge, LogisticRegression
from sklearn.datasets import make_regression, make_classification

X, y = make_regression(n_samples=100, n_features=10, noise=10, random_state=42)
alphas = [0.01, 1, 100, 10000]

ridge_w = []
lasso_w = []

for a in alphas:
    ridge = Ridge(alpha=a)
    lasso = Lasso(alpha=a, max_iter=10000)
    ridge.fit(X, y)
    lasso.fit(X, y)
    ridge_w.append(ridge.coef_)
    lasso_w.append(lasso.coef_)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for i, a in enumerate(alphas):
    axes[0].plot(ridge_w[i], 'o-', label=f'a={a}')
    axes[1].plot(lasso_w[i], 'o-', label=f'a={a}')

axes[0].set_title('L2')
axes[1].set_title('L1')

for ax in axes:
    ax.set_xlabel("Признак")
    ax.set_ylabel("Вес")
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()

huge_alpha = 1e10
model = Ridge(alpha=huge_alpha)
model.fit(X, y)
print(f"Веса {model.coef_}")
print(f"Bias {model.intercept_}")
print(f"Предсказания {model.predict(X[:3])}")

X_c, y_c = make_classification(n_samples=1000, n_features=20, random_state=42)
clf = LogisticRegression(C=1e-10, max_iter=10000)
clf.fit(X_c, y_c)

prob = clf.predict_proba(X_c)[:,1]
print("Var", np.std(prob))
print("Mean", prob.mean())