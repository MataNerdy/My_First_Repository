import numpy as np
from catboost import CatBoostClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(n_samples=1000000, n_features=100, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Начинаем обучение на GPU...")

gpu_model = CatBoostClassifier(
    task_type='GPU',
    devices='0',
    iterations=500,
    learning_rate=0.1,
    depth=6,
    verbose=100
)
gpu_model.fit(X_train, y_train)
gpu_model.save_model("catboost_model.cbm")