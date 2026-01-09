import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# 1. Load data
df = pd.read_csv('fraud_data.csv')

# 2. Advanced Cleaning & Feature Engineering
df = df[df['type'].isin(['TRANSFER', 'CASH_OUT'])]
df['type'] = df['type'].map({'TRANSFER': 0, 'CASH_OUT': 1})

# Add "Math Error" Features - This helps catch glitches vs fraud
df['errorBalanceOrig'] = df['newbalanceOrig'] + df['amount'] - df['oldbalanceOrg']
df['errorBalanceDest'] = df['oldbalanceDest'] + df['amount'] - df['newbalanceDest']

# Drop non-numeric and unnecessary columns
X = df.drop(['isFraud', 'step', 'nameOrig', 'nameDest', 'isFlaggedFraud'], axis=1)
y = df['isFraud']

# 3. Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train Random Forest (Better for Fraud Detection)
print("Training Random Forest Model... (This may take a minute)")
# class_weight='balanced' helps with the 99% vs 0.1% imbalance
rf_model = RandomForestClassifier(n_estimators=50, max_depth=10, class_weight='balanced', n_jobs=-1)
rf_model.fit(X_train, y_train)

# 5. Evaluation
print("\nImproved Model Evaluation:")
y_pred = rf_model.predict(X_test)
print(classification_report(y_test, y_pred))

# 6. Save the new model
joblib.dump(rf_model, 'improved_fraud_model.pkl')
print("Improved model saved!")