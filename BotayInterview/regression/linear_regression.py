import torch

class LinearRegression:
    def __init__(self, input_dim, learning_rate=0.01, max_iters=1000, tol=1e-6):
        # количество входных признаков
        self.input_dim = input_dim
        # гиперпараметры обучения
        # Скорость обучения (learning rate) — определяет размер шага при обновлении весов
        self.learning_rate = learning_rate
        # Максимальное количество итераций (iterations) — определяет, сколько раз мы будем обновлять веса
        self.max_iters = max_iters
        # Порог остановки обучения (tolerance) — определяет, насколько должна уменьшиться функция потерь, чтобы остановить обучение
        self.tol = tol
        # инициализация весов и смещения случайными значениями
        # requires_grad=True нужно, чтобы PyTorch считал градиенты по этим параметрам
        self.weights = torch.randn(input_dim, requires_grad=True)
        self.bias = torch.randn(1, requires_grad=True)

    def train(self, X, y):
        # проверяем, что число признаков в X совпадает с ожидаемым input_dim
        assert X.shape[1] == self.input_dim, f"Ожидалось {self.input_dim} признаков, получено {X.shape[1]}"
        # проверяем, что для каждого объекта из X есть соответствующее значение y
        assert X.shape[0] == y.shape[0], "X и y должны иметь одинаковое количество строк"

        # Храним значение функции потерь с прошлой итерации
        # Это нужно для ранней остановки обучения модели
        prev_loss = float('inf')

        for i in range(self.max_iters):
            # Forward pass: считаем предсказание линейной модели
            # y = Xw + b
            y_pred = X @ self.weights + self.bias
            # Считаем функцию потерь MSE - средний квадрат ошибки
            # MSE помогает оценить, насколько предсказания модели отличаются от реальных значений
            loss = torch.mean((y_pred - y) ** 2)
            # Backward pass: PyTorch автоматически считает градиенты
            # loss по weights и bias
            loss.backward()
            # Обновляем параметры вручную
            # torch.no_grad() нужен, чтобы PyTorch не добавлял это обновление в граф вычислений
            with torch.no_grad():
                self.weights -= self.learning_rate * self.weights.grad
                self.bias -= self.learning_rate * self.bias.grad
                # Обнуляем градиенты после шага оптимизации
                # Если этого не сделать, PyTorch будет накапливатьградиенты
                self.weights.grad.zero_()
                self.bias.grad.zero_()
            # Early_stopping:
            # если loss почти перестал меняться, обучение нужно остановить
            if abs(prev_loss - loss.item()) < self.tol:
                break
            # сохраняем текущее значение loss для сравнения на следующей итерации
            prev_loss = loss.item()

    def predict(self, X):
        # Во время предсказания градиенты не нужны
        with torch.no_grad():
            # вычисляем предсказание модели
            return X @ self.weights + self.bias