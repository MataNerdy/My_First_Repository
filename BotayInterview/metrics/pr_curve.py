import numpy as np
from sklearn.metrics import auc

y_true = np.array([0, 1, 0, 1, 0, 0, 1])
y_scores = np.array([0.2, 0.9, 0.4, 0.8, 0.1, 0.3, 0.85])

sorted_indices = np.argsort(y_scores)[::-1]
y_true_sorted = y_true[sorted_indices]
print(sorted_indices)
print(y_true_sorted)

tp = 0
fp = 0
precisions = [1.0]
recalls = [0.0]

total_positive = sum(y_true)
for label in y_true_sorted:
    if label == 1:
        tp += 1
    else:
        fp += 1
    pr = tp / (tp + fp)
    re = tp / total_positive
    precisions.append(pr)
    recalls.append(re)
    print(f"{tp=} {fp=} {pr=} {re=}")

auc_pr = auc(recalls, precisions)
print(auc_pr)