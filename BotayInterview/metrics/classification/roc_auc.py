import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import auc, confusion_matrix, roc_curve
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

tree = DecisionTreeClassifier(random_state=1, max_depth=5, min_samples_leaf=5)
tree.fit(X_train, y_train)
y_pred = tree.predict(X_test)
pred_proba = tree.predict_proba(X_test)
print(y_pred)

df_pred = pd.DataFrame({
    'proba': pred_proba[:, 1],
    'label': y_test
})

df_pred = df_pred.sort_values(by='proba')

TPRs = [0]
FPRs = [0]

thrs = df_pred['proba'].unique()[::-1]

def my_roc_curve(thrs):
    df_pred['pred_label'] = (df_pred['proba'] >= thrs).astype('int')
    print(df_pred)

    cls_1 = df_pred[df_pred.label == 1]
    cls_0 = df_pred[df_pred.label == 0]

    cm = confusion_matrix(df_pred['label'], df_pred['pred_label'])
    sns.heatmap(cm, annot=True)
    plt.ylabel('Groud truth')
    plt.xlabel('Prediction')
    plt.show()

    TN, FP, TP, FN = cm[0, 0], cm[0, 1], cm[1, 1], cm[1, 0]
    tpr = TP/(TP + FN)
    fpr = FP/(FP + TN)
    print('TPR 0.5:', TP/(TP + FN))
    print('FPR 0.5:', FP/(FP + TN))

    plt.scatter(np.arange(len(cls_1)), cls_1['proba'], label='class 1')
    plt.scatter(np.arange(len(cls_1), len(cls_1)+len(cls_0)), cls_0['proba'], label='class 0')
    plt.plot([-0.2, len(df_pred)], [thrs, thrs], c='b')
    plt.title('Вероятность быть 1 классом')
    plt.legend()
    plt.show()

    TPRs.append(tpr)
    FPRs.append(fpr)

    plt.plot(FPRs, TPRs, marker='o')
    plt.ylim([0, 1.1])
    plt.xlim([0, 1.1])
    plt.ylabel('TPR')
    plt.xlabel('FPR')
    plt.title('ROC_curve')
    plt.show()

for t in thrs:
    my_roc_curve(t)

print('AUC:', auc(FPRs, TPRs))

fprs, tprs, thr = roc_curve(df_pred['label'], df_pred['proba'])
print('AUC:', auc(fprs, tprs))

plt.plot(fprs, tprs, marker='o')
plt.ylim([0, 1.1])
plt.xlim([0, 1.1])
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC_curve')
plt.show()