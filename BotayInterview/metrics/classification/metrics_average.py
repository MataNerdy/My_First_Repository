import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)

clients = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
first_model = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
second_model = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0]

df = pd.DataFrame({
    'clients': clients,
    'first_model': first_model,
    'second_model': second_model
})

dct = {
    "true": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "pred": [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
}

df = pd.DataFrame(dct)
df['correct'] = df['true'] == df['pred']
df['correct_0'] = (df['correct']) & (df['true'] == 0)
df['correct_1'] = (df['correct']) & (df['true'] == 1)

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
F1_1 = 2*Pr_1*Re_1 / (Pr_1 + Re_1)

Acc_0 = (TP_0 + TN_0) / (TP_0 + TN_0 + FP_0 + FN_0)
Pr_0 = TP_0 / (TP_0 + FP_0)
Re_0 = TP_0 / (TP_0 + FN_0)
F1_0 = 2*Pr_0*Re_0 / (Pr_0 + Re_0)

TP_full = df['correct_0'].sum() + df['correct_1'].sum()
micro = TP_full / df.shape[0]
print(micro)

micro_pr = precision_score(df['true'], df['pred'], average='micro')
micro_re = recall_score(df['true'], df['pred'], average='micro')
micro_f1 = f1_score(df['true'], df['pred'], average='micro')
acc = accuracy_score(df['true'], df['pred'])
print("Micro:")
print(f"{micro_pr=} {micro_re=} {micro_f1=} {acc=}")

print("Macro:")
print(f"Pr = {(Pr_0 + Pr_1)/2:.2f} {precision_score(df['true'], df['pred'], average='macro'):.2f}")
print(f"Re = {(Re_0 + Re_1)/2:.2f} {recall_score(df['true'], df['pred'], average='macro'):.2f}")
print(f"F1 = {(F1_0 + F1_1)/2:.2f} {f1_score(df['true'], df['pred'], average='macro'):.2f}")

z = (df['true'] == 0).sum()
o = (df['true'] == 1).sum()
t = df['true'].shape[0]
print(z, o, t)

print("Weighted:")
print(f"Pr = {(z/t)*Pr_0 + (o/t)*Pr_1:.2f} {precision_score(df['true'], df['pred'], average='weighted'):.2f}")
print(f"Re = {(z/t)*Re_0 + (o/t)*Re_1:.2f} {recall_score(df['true'], df['pred'], average='weighted'):.2f}")
print(f"F1 = {(z/t)*F1_0 + (o/t)*F1_1:.2f} {f1_score(df['true'], df['pred'], average='weighted'):.2f}")

print(classification_report(df['true'], df['pred']))