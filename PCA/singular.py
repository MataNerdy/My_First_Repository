import numpy as np

np.random.seed(0)

n_total = 1000 # число образов выборки
n_features = 200 # число признаков

table = np.zeros(shape=(n_total, n_features))

for _ in range(100):
    i, j = np.random.randint(0, n_total), np.random.randint(0, n_features)
    table[i, j] = np.random.randint(1, 10)

N = len(table)
F = 1/N * table.T @ table
L, W = np.linalg.eig(F)
W = W.T

WW = sorted(zip(L, W), key=lambda lx: lx[0], reverse=True)
WW = np.array([w[1] for w in WW])

L = np.flip(np.sort(L))

data_x = table @ WW.T
indx_l = np.where(L < 0.01)[0][0]
data_x = data_x[:, :indx_l]
print(data_x.shape)