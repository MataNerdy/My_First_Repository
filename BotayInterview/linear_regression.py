import torch
import torch.nn as nn

class LinearRegression:
    def __init__(self, input_dim, learning_rate=0.01, max_iters=1000, tol=1e-6):
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.max_iters = max_iters
        self.tol = tol

        self.weights = torch.randn(input_dim, requires_grad=True)
        self.bias = torch.randn(1, requires_grad=True)

    def train(self, X, y):
        assert X.shape[1] == self.input_dim, f"Ожидалось {self.input_dim} признаков, получено {X.shape[1]}"
        assert X.shape[0] == y.shape[0], "X и y должны иметь одинаковое количество строк"

        prev_loss = float('inf')

        for i in range(self.max_iters):
            y_pred = X @ self.weights + self.bias
            loss = torch.mean((y_pred - y) ** 2)
            loss.backward()

            with torch.no_grad():
                self.weights -= self.learning_rate * self.weights.grad
                self.bias -= self.learning_rate * self.bias.grad

                self.weights.grad.zero_()
                self.bias.grad.zero_()

            if abs(prev_loss - loss.item()) < self.tol:
                break

            prev_loss = loss.item()

    def predict(self, X):
        with torch.no_grad():
            return X @ self.weights + self.bias