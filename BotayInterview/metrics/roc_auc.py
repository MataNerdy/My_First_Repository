import numpy as np
from sklearn.metrics import average_precision_score, precision_score, roc_auc_score

y_true = np.array([0, 0, 1, 1, 1])

scores_model1 = np.array([0.4, 0.45, 0.55, 0.6, 0.65])
scores_model2 = np.array([0.01, 0.02, 0.98, 0.99, 0.995])

print("AUC model 1:", roc_auc_score(y_true, scores_model1))
print("AUC model 2:", roc_auc_score(y_true, scores_model2))

pred1 = (scores_model1 > 0.5).astype(int)
pred2 = (scores_model2 > 0.5).astype(int)

print("Precision model 1:", precision_score(y_true, pred1))
print("Precision model 2:", precision_score(y_true, pred2))

y_true_all = np.concatenate([np.zeros(900), np.ones(100)])
y_scores_old = np.random.beta(2, 5, 900).tolist() + np.random.beta(2, 5, 100).tolist()
y_scores_new = np.random.beta(1, 6, 900).tolist() + np.random.beta(3, 3, 100).tolist()

print("AUC model old:", roc_auc_score(y_true_all, y_scores_old))
print("AUC model new:", roc_auc_score(y_true_all, y_scores_new))

pos_mask = y_true_all == 1
print("Average precision old:", average_precision_score(y_true_all[pos_mask], np.array(y_scores_old)[pos_mask]))
print("Average precision new:", average_precision_score(y_true_all[pos_mask], np.array(y_scores_new)[pos_mask]))
