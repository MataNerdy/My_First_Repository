import pandas as pd
from sklearn.metrics import classification_report

dct = {
    "true": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "pred": [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
}

df = pd.DataFrame(dct)
print(classification_report(df['true'], df['pred']))