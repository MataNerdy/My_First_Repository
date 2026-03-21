import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

df = pd.read_csv('/Users/Di/Documents/GitHub/My projects/My_First_Repository/AI_Education/EDA_students/eda_students_final.csv')

X = df.drop(['math score success', 'reading score success', 'writing score success', 'writing score', 'overall success'], axis=1)
y = df["writing score success"]

X['lunch'] = X['lunch'].map({'standard' : 1, 'free/reduced' : 0})
X['test preparation course'] = X['test preparation course'].map({"completed" : 1, "none" : 0})
X = X.drop(['parental level of education', 'class_group', 'gender'], axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)
pred = model.predict(X_test)

print(f"\n{y_test.value_counts(normalize=True)}")
print(f"\nWrong predictions: {sum(abs(y_test-pred))}\n")
print(f"\nConfusion_matrix:\n{confusion_matrix(y_test, pred)}\n")
print(f"\nWeights:{model.coef_}")
