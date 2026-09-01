import numpy as np


def func(x):
    return 0.5 * x + 0.2 * x ** 2 - 0.05 * x ** 3 + 0.2 * np.sin(4 * x) - 3


coord_x = np.arange(-4.0, 6.0, 0.1)
coord_y = func(coord_x)
coord_y = coord_y - np.mean(coord_y)  # центрирование функции

K = 10
X = np.array([[xx**i for i in range(K)] for xx in coord_x]) # обучающая выборка для поиска коэффициентов модели
Y = coord_y

X_train = X[::2]  # обучающая выборка (входы)
Y_train = Y[::2]  # обучающая выборка (целевые значения)

F = X.T @ X
L, W = np.linalg.eig(F)
sort_ind = np.argsort(L)[::-1]
WW = W[:,sort_ind]
G = np.dot(X, WW)[:,:7]
XX_train = G[::2]
w = np.linalg.inv(XX_train.T @ XX_train) @ XX_train.T @ Y_train
predict = np.dot(G, w)