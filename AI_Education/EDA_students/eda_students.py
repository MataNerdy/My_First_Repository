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

print(f"\nMean math score among women: {df[df["gender"] == "female"]["math score"].mean()}\n")
print(f"Mean math score among men: {df[df["gender"] == "male"]["math score"].mean()}\n")

plt.figure(figsize=(6,4))
plt.title("Math score vs gender")
sns.barplot(x='gender', y='math score', hue='gender', errorbar="sd", data=df, palette='summer', legend=False)
plt.savefig("sd_math_vs_gender.png")
plt.close()

print(f"\nDistribution of lunch type:\n\n{df["lunch"].value_counts()}")
df["lunch"] = df["lunch"].replace('standart', 'standard')
print(f"\nDistribution of lunch type:\n\n{df["lunch"].value_counts()}")

plt.figure(figsize=(6,4))
plt.title("Math score vs lunch")
sns.barplot(x='lunch', y='math score', hue='lunch', data=df, palette='summer', legend=False)
plt.savefig("math_vs_lunch.png")
plt.close()

plt.figure(figsize=(6,4))
plt.title("Math score vs gender & lunch")
sns.barplot(x='gender', y='math score', hue='lunch', data=df, palette='summer', legend=True)
plt.savefig("math_vs_gender_&_lunch.png")
plt.close()


plt.figure(figsize=(6,4))
plt.title("Math score vs gender & lunch")
sns.boxplot(x='lunch', y='math score', hue='lunch', data=df)
plt.savefig("boxplot_math_vs_lunch.png")
plt.close()

passmark = 50

for col in numeric_cols:
    df[f"{col} success"] = df[col].apply(lambda x: 1 if x >= passmark else 0)

df["overall success"] = (df["math score success"]+df["reading score success"]+df["writing score success"] == 3)
df[['math score success', 'reading score success', 'writing score success', 'overall success']].to_csv("success.csv", index=False)

print(f"\nAbsolute success:\n\n{len(df[df['overall success'] == 0]) / len(df)}")

print(f"\n\nParental level of education:\n\n{df['parental level of education'].value_counts()}")

plt.figure(figsize=(10,4))
plt.title("Math score vs parental level of education")
sns.barplot(x='parental level of education', y='math score', hue='parental level of education', data=df, palette='summer', legend=False)
plt.savefig("Math score vs parental level of education")
plt.close()

plt.figure(figsize=(10,5))
plt.title("Math success vs parental level of education")
p = sns.countplot(x='parental level of education', data = df, hue='math score success', palette='bright')
_ = plt.setp(p.get_xticklabels(), rotation=90)
plt.savefig("Math success vs parental level of education.png")
plt.close()

print(f"\n\nTest preparation course:{df['test preparation course'].value_counts()}")

plt.figure(figsize=(6,4))
plt.title("Math score vs test preparation course")
sns.barplot(x='test preparation course', y='math score', hue='test preparation course', data=df, palette='summer', legend=False)
plt.savefig("Math score vs test preparation course.png")
plt.close()

plt.figure()
plt.title("Math success vs test preparation course")
p = sns.countplot(x='test preparation course', data = df, hue='math score success', palette='bright')
plt.savefig("Math success vs test preparation course.png")
plt.close()

df.to_csv("eda_students_final.csv", index=False)