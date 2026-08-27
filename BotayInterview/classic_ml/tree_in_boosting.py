import numpy as np
import xgboost as xgb
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import GradientBoostingRegressor

y = np.array([1, 2, 3, 4, 5])
X = np.random.randn(5, 2)

gb = GradientBoostingRegressor(n_estimators=1, learning_rate=1.0)
gb.fit(X, y)
print(f"F0 (implicit): {gb.init_.constant_[0][0]}")

init = DummyRegressor(strategy='mean')
init.fit(X, y)
gb2 = GradientBoostingRegressor(n_estimators=1, init=init, learning_rate=1.0)
gb2.fit(X, y)

dtrain = xgb.DMatrix(X, label=y)
params = {'base_score': y.mean(), 'objective': 'reg:squarederror'}
model = xgb.train(params, dtrain, num_boost_round=1)