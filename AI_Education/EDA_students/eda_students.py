import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/Di/Documents/GitHub/My projects/My_First_Repository/AI_Education/EDA_students/students.csv')
print(f"\nHead of dataframe:\n\n{df.head()}")
print(f"\nShape of dataframe:\n\n{df.shape}")
print("\nInformation about dataframe:\n")
df.info()
print(f"\nDescription of dataframe:\n\n{df.describe()}")
print(f"\nScores of students :\n\n{df[['math score','reading score', 'writing score']].describe()}")

numeric_cols = df.select_dtypes(include=np.number).columns

for col in numeric_cols:
    plt.figure()
    sns.histplot(df[col], kde=True)
    plt.title(f"Distribution of {col}")
    plt.savefig(f"{col}_hist.png")
    plt.close()

df['math score'] = np.where(df['math score'] < 0, 0, df['math score'])
df['reading score'] = df['reading score'].fillna(df['reading score'].mean())
df['math score'] = df['math score'].fillna(df['math score'].mean())

print(f"\nScores of students :\n\n{df[['math score','reading score', 'writing score']].describe()}")

plt.figure()
plt.title("Heatmap of scores")
corr = df[['math score','reading score', 'writing score']].corr()
sns.heatmap(corr, cmap='crest')
plt.savefig("heatmap.png")
plt.close()

print(f"\nDistribution of genders:\n\n{df["gender"].value_counts(dropna=False, normalize=True)}")
df['gender'] = df['gender'].fillna("unknown")

print(f"\nDistribution of genders:\n\n{df["gender"].value_counts(dropna=False)}")

plt.figure(figsize=(6,4))
plt.title("Histogram of genders")
sns.countplot(x = "gender", hue="gender", data = df, palette='bright', legend=False)
plt.savefig("Hist of genders.png")
plt.close()

plt.figure(figsize=(6,4))
plt.title("Math score vs gender")
sns.barplot(x='gender', y='math score', hue='gender', data=df, palette='summer', legend=False)
plt.savefig("math_vs_gender.png")
plt.close()