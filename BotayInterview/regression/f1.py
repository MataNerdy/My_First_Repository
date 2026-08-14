from sklearn.metrics import f1_score
from sklearn.metrics import precision_score, recall_score
y_true = [0, 1, 1, 0, 1]
y_pred = [0, 1, 0, 0, 1]
score = f1_score(y_true, y_pred)
print(score)

f1_micro = f1_score(y_true, y_pred, average='micro')
f1_macro = f1_score(y_true, y_pred, average='macro')


y_true = [0, 0, 0, 0, 1]      # 80% класс 0, 20% класс 1
y_pred = [0, 0, 0, 0, 0]      # модель всегда предсказывает 0

# Micro: считает глобально
print("Precision micro:", precision_score(y_true, y_pred, average='micro'))  # 0.8
print("Recall micro:   ", recall_score(y_true, y_pred, average='micro'))     # 0.8

# Macro: среднее по классам
# Класс 0: prec=1.0, rec=1.0
# Класс 1: prec=0.0, rec=0.0
print("Precision macro:", precision_score(y_true, y_pred, average='macro'))  # 0.5
print("Recall macro:   ", recall_score(y_true, y_pred, average='macro'))     # 0.5