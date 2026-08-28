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

print("Переходим к инференсу на CPU...")

cpu_model = CatBoostClassifier()
cpu_model.load_model('/content/catboost_model.cbm')

sample_data = X_test[:1000]
predictions_cpu = cpu_model.predict(sample_data)
predictions_gpu = gpu_model.predict(sample_data)
assert np.array_equal(predictions_cpu, predictions_gpu), \
  "Предсказания должны быть идентичны, независимо от устройства обучения"

print(f"Успешно выполнено предсказание для {len(sample_data)} объектов на CPU.")
print("Модель готова к деплою в production без видеокарты.")
