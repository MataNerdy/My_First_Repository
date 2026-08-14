import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve, cross_val_score

X, y = make_classification(n_samples=200, n_features=50, n_informative=10, n_redundant=40, random_state=42)
model_weak_reg = LogisticRegression(C=0.1, max_iter=1000)
model_no_reg = LogisticRegression(C=1e9, max_iter=1000)

train_sizes, train_scores, val_scores = learning_curve(model_no_reg, X, y, cv=5, scoring="neg_log_loss", n_jobs=-1)

train_loss = - train_scores.mean(axis=1)
val_loss = - val_scores.mean(axis=1)

plt.plot(train_sizes, train_loss, 'o-', label='Train log-loss')
plt.plot(train_sizes, val_loss, 'o-', label='Validation log-loss')
plt.ylabel('Log-loss')
plt.xlabel('Размер обучающей выборки')
plt.title('Кривые обучения: признаков больше, чем нужно → переобучение')
plt.legend()
plt.grid(True)
plt.show()


score_reg = cross_val_score(model_weak_reg, X, y, cv=5, scoring='roc_auc').mean()
score_no_reg = cross_val_score(model_no_reg, X, y, cv=5, scoring='roc_auc').mean()
print(f"С регуляризацией (C=0.1): AUC = {score_reg:.3f}")
print(f"Без регуляризации (C=1e9): AUC = {score_no_reg:.3f}")