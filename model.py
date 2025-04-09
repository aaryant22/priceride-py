import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt

def load_and_preprocess(filepath):
    data = pd.read_excel(filepath)
    features = ['exshowroom', 'make', 'power', 'torque']
    target = 'insurance'
    data = data[features + [target]].copy()
    
    z_scores = (data[target] - data[target].mean()) / data[target].std()
    data = data[abs(z_scores) < 4]

    # Q1 = data[target].quantile(0.02)
    # Q3 = data[target].quantile(0.98)
    # data = data[(data[target] >= Q1) & (data[target] <= Q3)]
    
    data['exshowroom_log'] = np.log1p(data['exshowroom'])
    data['power_torque_ratio'] = data['power'] / data['torque']
    
    # One-Hot Encoding for 'make'
    data = pd.get_dummies(data, columns=['make'], drop_first=True)
    
    return data.drop(columns=[target]), data[target]

X, y = load_and_preprocess(os.getenv("FILE_NAME"))

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Optimal optuna params
best_params = {
    'n_estimators': 300,
    'max_depth': 6,
    'learning_rate': 0.05,
    'subsample': 0.9,
    'colsample_bytree': 0.9,
    'reg_alpha': 0.1,
    'objective': 'reg:squarederror',
    'random_state': 42
}

model = xgb.XGBRegressor(**best_params)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("\nModel Performance:")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R²: {r2_score(y_test, y_pred):.2f}")

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
plt.xlabel('Actual Insurance (₹)')
plt.ylabel('Predicted Insurance (₹)')
plt.title('Actual vs Predicted Insurance Costs')
plt.grid(True)
plt.show()

residuals = y_test - y_pred
plt.figure(figsize=(10, 6))
plt.scatter(y_pred, residuals, alpha=0.6)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values (₹)')
plt.ylabel('Residuals (Actual - Predicted)')
plt.title('Residual Analysis')
plt.grid(True)
plt.show()

def predict_insurance(exshowroom, power, torque, make):
    input_data = pd.DataFrame({
        'exshowroom': [exshowroom],
        'power': [power],
        'torque': [torque],
        'exshowroom_log': [np.log1p(exshowroom)],
        'power_torque_ratio': [power / torque]
    })
    
    for col in X.columns:
        if col.startswith('make_'):
            input_data[col] = 0
    if f'make_{make}' in X.columns:
        input_data[f'make_{make}'] = 1
    
    return model.predict(input_data[X.columns])[0]

# Example usage
prediction = predict_insurance(
    exshowroom=1500000,
    power=106,
    torque=90,
    make='BMW'
)
budget_prediction = predict_insurance(
    exshowroom=300000,
    power=40,
    torque=39,
    make='KTM'
)
mid_prediction = predict_insurance(
    exshowroom=330000,
    power=47,
    torque=52,
    make='Royal Enfield'
)
print(f"\nPredicted Insurance: ₹{prediction:.2f}")
print(f"\nPredicted Insurance: ₹{budget_prediction:.2f}")
print(f"\nPredicted Insurance: ₹{mid_prediction:.2f}")