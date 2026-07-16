import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve
from sklearn.datasets import make_classification
from sklearn.metrics import log_loss

# Искусственные данные с потенциалом переобучения
X, y = make_classification(n_samples=200, n_features=50, n_informative=10, n_redundant=40, random_state=42)

# Модель без регуляризации (C очень большой → почти нет штрафа)
model = LogisticRegression(C=1e9, max_iter=1000)

train_sizes, train_scores, val_scores = learning_curve(
    model, X, y, cv=5, scoring='neg_log_loss', n_jobs=-1
)

train_loss = -train_scores.mean(axis=1)
val_loss = -val_scores.mean(axis=1)

plt.plot(train_sizes, train_loss, 'o-', label='Train log-loss')
plt.plot(train_sizes, val_loss, 'o-', label='Validation log-loss')
plt.xlabel('Размер обучающей выборки')
plt.ylabel('Log-loss')
plt.title('Кривые обучения: признаков больше, чем нужно → переобучение')
plt.legend()
plt.grid(True)
plt.show()