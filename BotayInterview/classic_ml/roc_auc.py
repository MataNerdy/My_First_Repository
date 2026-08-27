from sklearn.metrics import roc_auc_score

y_true = [0, 0, 1, 1]
y_score = [0.2, 0.4, 0.6, 0.8]

y_true_duplicated = [0]*7*2 + [1]*4*2
y_score_duplicated = [0.2]*7 + [0.4]*7 + [0.6]*4 + [0.8]*4

auc_original = roc_auc_score(y_true, y_score)
auc_duplicated = roc_auc_score(y_true_duplicated, y_score_duplicated)

print(f"Original AUC: {auc_original:.3f}")
print(f"Duplicated AUC: {auc_duplicated:.3f}")