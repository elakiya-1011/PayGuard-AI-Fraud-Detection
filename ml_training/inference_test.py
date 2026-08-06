import joblib, pandas as pd, numpy as np
from pathlib import Path

# Project root (Desktop folder)
PROJECT_ROOT = Path(r'C:/Users/Pranavikha/Desktop/GENAI TRAINING')
DATA_DIR = PROJECT_ROOT / 'data' / 'datasets'
MODEL_DIR = PROJECT_ROOT / 'data' / 'trained_model'

# Load artifacts
pipeline = joblib.load(MODEL_DIR / 'preprocess.pkl')
model = joblib.load(MODEL_DIR / 'fraud_model.pkl')
label_encoder = joblib.load(MODEL_DIR / 'label_encoder.pkl')

# Read transactions CSV
df = pd.read_csv(DATA_DIR / 'payment_transactions.csv')
# Sample 5 rows
sample = df.sample(5, random_state=42).reset_index(drop=True)

# Identifier and target columns
IDENTIFIER_COLS = ['Transaction_ID', 'User_ID', 'Merchant_ID', 'Device_ID', 'Card_Number', 'IP_Address', 'Session_ID']
TARGET_COL = 'Fraud_Label'

# Prepare raw feature matrix
feature_cols = [c for c in df.columns if c not in IDENTIFIER_COLS + [TARGET_COL]]
X_raw = sample[feature_cols].values.astype(object)

# Transform features
X_pre = pipeline.transform(X_raw)

# Predict
pred = model.predict(X_pre)
proba = model.predict_proba(X_pre)
labels = label_encoder.inverse_transform(pred)

# Output results
for i, row in enumerate(sample.itertuples(index=False)):
    id_info = {col: getattr(row, col) for col in IDENTIFIER_COLS}
    print(f"Sample {i+1}:")
    print('Identifiers:', id_info)
    print('Predicted label:', labels[i])
    prob_dict = dict(zip(label_encoder.classes_, proba[i]))
    print('Class probabilities:', prob_dict)
    print('---')
