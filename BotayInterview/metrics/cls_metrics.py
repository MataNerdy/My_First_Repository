y_true = [1, 0, 1, 1, 0, 1, 0, 0, 1]
y_pred = [1, 0, 0, 1, 0, 1, 1, 0, 1]

TP = 0
FP = 0
TN = 0
FN = 0

for t, p in zip(y_true, y_pred):
    if t == 1 and p == 1:
        TP += 1
    elif t == 1 and p == 0:
        FN += 1
    elif t == 0 and p == 1:
        FP += 1
    else:
        TN += 1

print(f"{TP=} {FP=} {TN=} {FN=}")

Accuracy = (TP+TN)/(TP+TN+FP+FN)
Precision = (TP)/(TP+FN)
Recall = (TP)/(TP+FP)
F1_score = 2*Precision*Recall/(Precision+Recall)

print(f"{Accuracy=:.4f} {Precision=} {Recall=} {F1_score=:.4f}")