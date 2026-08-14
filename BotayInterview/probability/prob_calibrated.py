import numpy as np

y_true = np.random.binomial(1, 0.8, 100)
y_true_overconf = np.random.binomial(1, 0.6, 100)

uncalibrated_probs = np.array([0.9, 0.85, 0.8, 0.75, 0.7])
calibrated_probs = np.array([0.65, 0.62, 0.60, 0.58, 0.55])

print("До калибровки: 0.75 → ожидаем 75% дефолта")
print("После калибровки: 0.58 → ожидаем 58% дефолта — ближе к реальности")