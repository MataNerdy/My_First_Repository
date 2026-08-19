import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import (
    auc,
    precision_recall_curve,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

matplotlib.rcParams.update({'font.size': 14})
pd.set_option('display.max_columns', 10)

data = load_breast_cancer()
X = pd.DataFrame(data['data'], columns=data['feature_names'])
y = pd.Series(data['target'])

np.random.seed(5)
features = np.random.randint(X.shape[1], size=2)
X_train, X_test, y_train, y_test = train_test_split(X.iloc[:, features], y, test_size=9, random_state=4)

def pr(threshold=0.5):

    pred = np.where(pred_proba[:, 1] >= threshold, 1, 0)
    p = precision_score(y_test, pred)
    r = recall_score(y_test, pred)
    return p, r


tree = DecisionTreeClassifier(random_state=1, max_depth=5, min_samples_leaf=5)
tree.fit(X_train, y_train)
pred_proba = tree.predict_proba(X_test)

df_prob = pd.DataFrame({
    'proba': pred_proba[:, 1],
    'label': y_test
})

df_prob = df_prob.sort_values(by='proba')

precision, recall, thresholds = precision_recall_curve(df_prob['label'], df_prob['proba'])
plt.plot(recall, precision, marker='o')
plt.ylim([0, 1.1])
plt.xlim([0, 1.1])
plt.xlabel("Recall")
plt.ylabel("Precision")
plt.show()

print(f"PR-AUC: {auc(recall, precision)}")

prs = [1]
rcs = [0]

trsh = [0, 0.54, 0.84, 0.966, 0.968, 1][::-1]
for t in trsh:
    p, r = pr(t)
    prs.append(p)
    rcs.append(r)
    plt.plot(rcs, prs, marker='o')
    plt.ylim([0, 1.1]);plt.xlim([0, 1.1])
    plt.xlabel('Recall');plt.ylabel('Precision')
    plt.title('PR_curve')
    plt.show()

print(f"PR-AUC: {auc(rcs, prs)}")

trsh = 1
print(df_prob)

cls_1 = df_prob[df_prob['label'] == 1]
cls_0 = df_prob[df_prob['label'] == 0]

p, r = pr(trsh)
print(f"Precision={p}, Recall={r}")

plt.scatter(np.arange(len(cls_1)), cls_1["proba"], label='class 1')
plt.scatter(np.arange(len(cls_1), len(cls_1)+len(cls_0)), cls_0["proba"], label='class 0')
plt.plot([-0.2, len(df_prob)], [trsh, trsh], c='b')
plt.title('Вероятность быть 1 классом')
plt.legend()
plt.show()