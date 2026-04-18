import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

df = pd.read_csv("/Users/Di/Documents/GitHub/My projects/My_First_Repository/ML/house_prices.csv")
print(df.head())
print(df.shape)

X = df.drop('median_house_value', axis=1)
y = df['median_house_value']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = LinearRegression()

model.fit(X_train, y_train)
prediction = model.predict(X_test)
print(prediction[:10])
print(mean_squared_error(y_test, prediction)**0.5)
