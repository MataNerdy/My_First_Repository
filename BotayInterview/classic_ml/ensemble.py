import numpy as np
from sklearn.datasets import make_regression
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

X, y = make_regression(n_samples=1000, n_features=20, noise=10, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

rf = RandomForestRegressor(n_estimators=100, random_state=42)
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
ridge = Ridge(alpha=1.0)

rf.fit(X_train, y_train)
gb.fit(X_train, y_train)
ridge.fit(X_train, y_train)

pred_rf = rf.predict(X_test)
pred_gb = gb.predict(X_test)
pred_ridge = ridge.predict(X_test)

pred_ensemble = (pred_rf + pred_gb + pred_ridge) / 3

print(f"RF MSE: {mean_squared_error(y_test, pred_rf)}")
print(f"GB MSE: {mean_squared_error(y_test, pred_gb)}")
print(f"Ridge MSE: {mean_squared_error(y_test, pred_ridge)}")
print(f"Ensemble MSE: {mean_squared_error(y_test, pred_ensemble)}")

def expert_1(x):
    return 2 * x[:,0] + 1

def expert_2(x):
    return np.sin(x[:,1]) * 10

def gating_network(x):
    return (x[:,0] > 0).astype(float)

x_sample = np.random.randn(1000, 2)
gate = gating_network(x_sample)
output = gate * expert_1(x_sample) + (1 - gate) * expert_2(x_sample)