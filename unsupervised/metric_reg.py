import numpy as np

# координаты четырех точек
x = np.array([0, 1, 2, 3])
y = np.array([0.5, 0.8, 0.6, 0.2])

x_est = np.arange(0, 3.1, 0.1) # множество точек для промежуточного восстановления функции

h = 1
y_est = []

for x0 in x_est:
    n = 0.0
    d = 0.0
    for  xi, yi in zip(x, y):
        r = abs(xi - x0)/ h
        K = 1 - r if abs(r) <= 1 else 0
        n += yi * K
        d += K
    y_val = n / d if d != 0 else 0.0
    y_est.append(y_val)