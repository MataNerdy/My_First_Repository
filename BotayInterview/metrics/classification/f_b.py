import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report,
    f1_score,
    fbeta_score,
    precision_score,
    recall_score,
)


def f_beta(pr, re, b=1):
    return (1+b**2)*pr*re / (b**2*pr + re)

dct = {
    "true": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    "pred": [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
}

df = pd.DataFrame(dct)
df['res'] = df['true'] == df['pred']
print(df)

beta=0.25
pr = precision_score(df['true'], df['pred'])
re = recall_score(df['true'], df['pred'])
f1 = 2*pr*re / (pr + re)

print(f"{pr=} {re=} f1={f_beta(pr, re, 1):.2f} f_{beta}={f_beta(pr, re, beta):.2f}")
print(classification_report(df['true'], df['pred']))
print(f1_score(df['true'], df['pred']), fbeta_score(df['true'], df['pred'], beta=beta))

pr, re = np.meshgrid(np.linspace(0.01, 1, 100), np.linspace(0.01, 1, 100))
fb_levels = np.empty_like(pr)
for i in range(pr.shape[0]):
    for j in range(pr.shape[1]):
        fb_levels[i, j] = 1/2 * f_beta(pr[i, j], re[i, j], b=beta)

plt.figure(figsize = (6,6))
plt.title("F1")
plt.xlabel('precision')
plt.ylabel('recall')
plt.grid()

plt.contour(pr, re, fb_levels, levels=20)
plt.show()

pr, re = np.meshgrid(np.linspace(0.01, 1, 100), np.linspace(0.01, 1, 100))
mean_levels = np.empty_like(pr)
for i in range(pr.shape[0]):
    for j in range(pr.shape[1]):
        mean_levels[i, j] = 1/2 * (pr[i, j] + re[i, j])

plt.figure(figsize = (6,6))
plt.title("Mean")
plt.xlabel('precision')
plt.ylabel('recall')
plt.grid()

plt.contour(pr, re, mean_levels, levels=100)
plt.plot(0.1, 1, 'ro', ms=12)
plt.plot(0.55, 0.55, 'bo', ms=12)
plt.show()

min_level = np.empty_like(pr)
for i in range(pr.shape[0]):
    for j in range(pr.shape[1]):
            min_level[i, j] = min(pr[i, j], re[i, j])

plt.figure(figsize = (6,6))
plt.title("Min")
plt.xlabel('precision')
plt.ylabel('recall')
plt.grid()

plt.contour(pr, re, min_level, levels=100)
plt.plot(0.1, 1, 'ro', ms=12)
plt.plot(0.55, 0.55, 'bo', ms=12)
plt.show()

f1_level = np.empty_like(pr)

for i in range(pr.shape[0]):
     for j in range(pr.shape[1]):
          f1_level[i, j] = 2 / (1/pr[i, j] + 1/re[i, j])

plt.figure(figsize = (6,6))
plt.title("F1")
plt.xlabel('precision')
plt.ylabel('recall')
plt.grid()

plt.contour(pr, re, f1_level, levels=100)
plt.plot(0.1, 1, 'ro', ms=12)
plt.plot(0.55, 0.55, 'bo', ms=12)
plt.show()