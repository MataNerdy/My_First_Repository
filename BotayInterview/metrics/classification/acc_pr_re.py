import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sklearn.metrics

dct = {
    "true": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "pred": [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
}


df = pd.DataFrame(dct)

df["result"] = df["pred"] == df["true"]

TP_1 = df[(df["pred"] == df["true"]) & df["true"]].shape[0]
FP_1 = df[(df["pred"] != df["true"]) & df["pred"]].shape[0]
TN_1 = df[(df["pred"] == df["true"]) & ~df["true"]].shape[0]
FN_1 = df[(df["pred"] != df["true"]) & ~df["pred"]].shape[0]

TP_0 = df[(df["pred"] == df["true"]) & ~df["true"]].shape[0]
FP_0 = df[(df["pred"] != df["true"]) & ~df["pred"]].shape[0]
TN_0 = df[(df["pred"] == df["true"]) & df["true"]].shape[0]
FN_0 = df[(df["pred"] != df["true"]) & df["pred"]].shape[0]

Acc_1 = (TP_1 + TN_1) / (TP_1 + TN_1 + FP_1 + FN_1)
Pr_1 = TP_1 / (TP_1 + FP_1)
Re_1 = TP_1 / (TP_1 + FN_1)

Acc_0 = (TP_0 + TN_0) / (TP_0 + TN_0 + FP_0 + FN_0)
Pr_0 = TP_0 / (TP_0 + FP_0)
Re_0 = TP_0 / (TP_0 + FN_0)

print(f"{TP_1=}, {FP_1=}, {TN_1=}, {FN_1=}")
print(f"{Acc_1=} {Pr_1=} {Re_1=}")

print(f"{TP_0=}, {FP_0=}, {TN_0=}, {FN_0=}")
print(f"{Acc_0=} {Pr_0=:.2f} {Re_0=}")

print(f'for 1: Acc = {sklearn.metrics.accuracy_score(df["true"], df["pred"])}, Pr = {sklearn.metrics.precision_score(df["true"], df["pred"])}, Re = {sklearn.metrics.recall_score(df["true"], df["pred"])}')
print(sklearn.metrics.classification_report(y_pred=df["pred"], y_true=df["true"]))

cm = sklearn.metrics.confusion_matrix(df["true"], df["pred"])

sns.heatmap(cm, annot=True)
plt.title("Confusion matrix")
plt.xlabel("Prediction")
plt.ylabel("Ground truth")
plt.show()