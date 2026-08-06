"""
=========================================================
PayGuard AI
Model Inspection Utility

Purpose:
1. Verify model artifacts
2. Verify preprocessing pipeline
3. Verify expected input columns
4. Test one real prediction transformation
=========================================================
"""

from pathlib import Path
import joblib
import pandas as pd

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parent

MODEL_DIR = PROJECT_ROOT / "data" / "trained_model"

DATASET = PROJECT_ROOT / "data" / "datasets" / "payment_transactions.csv"

# ==========================================================
# Load Artifacts
# ==========================================================

print("\n" + "=" * 80)
print("LOADING ARTIFACTS")
print("=" * 80)

model = joblib.load(MODEL_DIR / "fraud_model.pkl")
preprocess = joblib.load(MODEL_DIR / "preprocess.pkl")
label_encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")

print("✅ fraud_model.pkl loaded")
print("✅ preprocess.pkl loaded")
print("✅ label_encoder.pkl loaded")

# ==========================================================
# Dataset
# ==========================================================

print("\n" + "=" * 80)
print("DATASET INFORMATION")
print("=" * 80)

df = pd.read_csv(DATASET)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print("\nColumn Names:\n")

for i, col in enumerate(df.columns, start=1):
    print(f"{i:02d}. {col}")

# ==========================================================
# Target Classes
# ==========================================================

print("\n" + "=" * 80)
print("LABEL CLASSES")
print("=" * 80)

print(label_encoder.classes_)

# ==========================================================
# Build Feature Columns
# ==========================================================

IDENTIFIER_COLUMNS = [
    "Transaction_ID",
    "Session_ID",
    "User_ID",
    "Merchant_ID",
    "Device_ID",
    "Card_Number",
    "IP_Address",
]

TARGET_COLUMN = "Fraud_Label"

feature_columns = [
    c
    for c in df.columns
    if c not in IDENTIFIER_COLUMNS + [TARGET_COLUMN]
]

print("\n" + "=" * 80)
print("FEATURES USED FOR MODEL")
print("=" * 80)

print(f"Total Features : {len(feature_columns)}")

for i, col in enumerate(feature_columns, start=1):
    print(f"{i:02d}. {col}")

# ==========================================================
# Sample Input
# ==========================================================

print("\n" + "=" * 80)
print("TESTING PREPROCESSING")
print("=" * 80)

sample = df[feature_columns].iloc[[0]]

print("Input Shape :", sample.shape)

try:

    transformed = preprocess.transform(sample.values.astype(object))

    print("✅ Transformation Successful")

    print("Output Shape :", transformed.shape)

except Exception as e:

    print("❌ Transformation Failed")

    print(type(e).__name__)

    print(e)

# ==========================================================
# Model Prediction
# ==========================================================

print("\n" + "=" * 80)
print("TESTING MODEL")
print("=" * 80)

try:

    prediction = model.predict(transformed)

    probability = model.predict_proba(transformed)

    label = label_encoder.inverse_transform(prediction)

    print("✅ Prediction Successful")

    print("Predicted Class :", label[0])

    print("Probabilities :")

    for cls, prob in zip(label_encoder.classes_, probability[0]):
        print(f"{cls:<15}: {prob:.4f}")

except Exception as e:

    print("❌ Prediction Failed")

    print(type(e).__name__)

    print(e)

# ==========================================================
# Preprocess Object
# ==========================================================

print("\n" + "=" * 80)
print("PREPROCESS OBJECT")
print("=" * 80)

print(preprocess)

print("\n" + "=" * 80)
print("INSPECTION COMPLETED")
print("=" * 80)
print("\n" + "=" * 80)
print("EXPECTED INPUT COLUMNS")
print("=" * 80)

try:
    ct = preprocess.named_steps["preprocess"]

    for name, transformer, cols in ct.transformers_:
        print(f"\n{name}")
        print(cols)

except Exception as e:
    print(e)