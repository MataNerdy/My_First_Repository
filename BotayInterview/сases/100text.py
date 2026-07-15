# Пример: обучение на вырожденных данных — 100 одинаковых текстов, метки [0,0,...,1]
# Показывает, что модель выдаёт ~0.01 для всех объектов

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss

# === Подготовка данных ===
text = "это один и тот же текст для всех примеров"
texts = [text] * 100  # 100 копий

# Метки: 99 нулей и одна единица (последний объект)
labels = np.array([0] * 99 + [1])

print(f"Число объектов: {len(texts)}")
print(f"Метки: 99×0, 1×1 → доля класса 1 = {labels.mean():.2f}")

# === Векторизация текстов (TF-IDF) ===
# Все тексты одинаковые → все векторы будут идентичны
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)  # shape: (100, num_features)

print(f"\nРазмерность признакового пространства: {X.shape[1]}")
print(f"Все векторы одинаковы? {np.allclose(X.toarray(), X[0].toarray())}")

# === Обучение логистической регрессии ===
# Используем solver, который поддерживает вероятностные выходы
model = LogisticRegression(
    solver='lbfgs',
    max_iter=1000,
    random_state=42
)
model.fit(X, labels)

# === Предсказания ===
proba = model.predict_proba(X)  # shape: (100, 2)
pred_class_1 = proba[:, 1]      # вероятность класса 1

print(f"\nПредсказанные вероятности для класса 1 (первые 5 и последний):")
print(f"  Первые 5: {pred_class_1[:5]}")
print(f"  Последний: {pred_class_1[-1]:.6f}")

# Все предсказания должны быть одинаковыми (входы одинаковые)
print(f"\nВсе предсказания одинаковы? {np.allclose(pred_class_1, pred_class_1[0])}")

# Сравним с оптимальным значением (априорная вероятность)
optimal_p = labels.mean()
predicted_p = pred_class_1[0]

print(f"\nАприорная вероятность класса 1: {optimal_p:.4f}")
print(f"Предсказанная вероятность:      {predicted_p:.4f}")
print(f"Разница:                       {abs(predicted_p - optimal_p):.4f}")

# Посчитаем лосс
loss = log_loss(labels, proba)
optimal_loss = log_loss(labels, np.full((100, 2), [1 - optimal_p, optimal_p]))

print(f"\nЛог-лосс модели:               {loss:.6f}")
print(f"Лог-лосс при p=0.01 (оптимум): {optimal_loss:.6f}")
print(f"→ Модель действительно близка к оптимальному решению!")

# === Что будет, если попытаться переобучиться? ===
# Попробуем без регуляризации (C очень большое)
overfit_model = LogisticRegression(solver='lbfgs', C=1e6, max_iter=10000, random_state=42)
overfit_model.fit(X, labels)
overfit_proba = overfit_model.predict_proba(X)[:, 1]

print(f"\nБез регуляризации (C=1e6):")
print(f"  Предсказанная вероятность: {overfit_proba[0]:.6f}")
print(f"  Лог-лосс: {log_loss(labels, overfit_model.predict_proba(X)):.6f}")
print("→ Даже при слабой регуляризации модель не переобучается, потому что все входы одинаковы!")