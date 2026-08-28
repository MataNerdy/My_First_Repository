import lightgbm as lgb
import xgboost as xgb
from catboost import CatBoostClasifier

model = xgb.XGBClassifier(
    reg_alpha=1.0,
    reg_lambda=1.0,
    objective='binary:logistic'
)
X, y = '', ''
train_data = lgb.Dataset(X, y, categorical_feature=['city', 'category'])
params = {
    'boosting_type': 'gbdt',
    'num_leaves': 31,
    'max_depth': -1
}

model = lgb.train(params, train_data)

model = CatBoostClasifier(
    cat_features=[0, 2],
    iterations=1000,
    loss_function='Logloss'
)
model.fit(X, y, verbose=False)
