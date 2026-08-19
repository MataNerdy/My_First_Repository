import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

X, y = load_digits(return_X_y=True)
print(X.shape, y.shape)


tree = DecisionTreeClassifier(max_depth=8, random_state=1)
tree.fit(X, y)
pred = tree.predict(X)
print(classification_report(y, pred))

plt.figure(figsize=(16, 10))
for i in range(15):
    plt.subplot(3, 5, i+1)
    plt.imshow(X[i,:].reshape(8, 8), cmap="gray")
plt.show()

y_freq = pd.Series(y).value_counts()
sns.barplot(x=y_freq.index, y=y_freq.values)
plt.yticks(np.linspace(0, 180, 10))
plt.show()

target = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
y_freq = pd.Series(target).value_counts()
sns.barplot(x=y_freq.index, y=y_freq.values)
plt.show()

pred = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
df = pd.DataFrame({
    'true': target,
    'pred': pred
})

print(classification_report(df['true'], df['pred']))

target = [0, 0, 0, 0, 0, 0, 0,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          2]

y_freq = pd.Series(target).value_counts()
sns.barplot(x=y_freq.index, y=y_freq.values)
plt.show()

pred = [0, 0, 0, 0, 0, 0, 0,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1]

df = pd.DataFrame({
    'true': target,
    'pred': pred
})

print(classification_report(df['true'], df['pred']))