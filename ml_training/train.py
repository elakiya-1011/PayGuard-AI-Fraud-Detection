import os
import joblib
import pandas as pd
import warnings
import importlib
import json
import datetime
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import (f1_score, recall_score, precision_score,
                             confusion_matrix, roc_auc_score, classification_report)
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
warnings.filterwarnings('ignore')

# ------------------- Load raw data and artifacts -------------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

csv_path = os.path.join(
    PROJECT_ROOT,
    "data",
    "datasets",
    "payment_transactions.csv"
)
raw_df = pd.read_csv(csv_path)

# Load fitted preprocessing pipeline and label encoder
MODEL_DIR = os.path.join(
    PROJECT_ROOT,
    "data",
    "trained_model"
)

preprocess = joblib.load(
    os.path.join(MODEL_DIR, "preprocess.pkl")
)

label_encoder = joblib.load(
    os.path.join(MODEL_DIR, "label_encoder.pkl")
)

# ------------------------------------------------------------
# Separate Features and Target
# Remove identifiers and leakage columns
# ------------------------------------------------------------

LEAKAGE_COLUMNS = [

    # Target
    "Fraud_Label",

    # Transaction identifiers
    "Transaction_ID",
    "User_ID",
    "Merchant_ID",
    "Device_ID",
    "Card_Number",
    "IP_Address",
    "Session_ID",

    # Personal identifiers
    "Customer_Name",
    "Phone_Number",
    "Email",
    "Account_Number",
    "UPI_ID",

    # Leakage columns
    "Fraud_Reason",
    "Risk_Score",
    "Confidence_Score",
    "Transaction_Status",

    # Derived leakage features
    "Amount_Category",
    "Is_High_Value",
    "Amount_vs_Average",
    "Merchant_High_Risk",
    "Merchant_Rating_Category",
    "IPAddress",

]

X_raw = raw_df.drop(
    columns=LEAKAGE_COLUMNS,
    errors="ignore"
)
print("\nFeatures used for training:")
print(X_raw.columns.tolist())

print("\nFeature count:")
print(len(X_raw.columns))

y_raw = raw_df["Fraud_Label"]

y = label_encoder.transform(y_raw)

# ------------------- Train/validation/test split (70/15/15) -------------------
X_temp, X_test, y_temp, y_test = train_test_split(
    X_raw, y, test_size=0.15, stratify=y, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.1765, stratify=y_temp, random_state=42)  # 0.1765*0.85≈0.15

# ------------------- Apply preprocessing (do NOT refit) -------------------
# Convert all feature values to object/string format
X_train = X_train.astype(object).astype(str)

X_val = X_val.astype(object).astype(str)

X_test = X_test.astype(object).astype(str)


X_train_processed = preprocess.transform(X_train)

X_val_processed = preprocess.transform(X_val)

X_test_processed = preprocess.transform(X_test)

# ------------------- Handle class imbalance with SMOTE (after preprocessing) -------------------
smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train_processed, y_train)

# ------------------- Define models and hyper‑parameter grids -------------------
models = {}
param_dist = {}

# XGBoost (if installed)
if importlib.util.find_spec('xgboost'):
    from xgboost import XGBClassifier
    models['xgboost'] = XGBClassifier(objective='multi:softprob', num_class=len(label_encoder.classes_), eval_metric='mlogloss', use_label_encoder=False, random_state=42)
    param_dist['xgboost'] = {
        'n_estimators': [100],
        'learning_rate': [0.05],
        'max_depth': [3],
        'subsample': [0.8],
        'colsample_bytree': [0.8]
    }

# Random Forest
# Random Forest
models['random_forest'] = RandomForestClassifier(
    random_state=42,
    class_weight="balanced"
)

param_dist['random_forest'] = {
    'n_estimators': [100],
    'max_depth': [10],
    'min_samples_split': [5]
}

# Logistic Regression
models['logistic_regression'] = LogisticRegression(solver='saga', max_iter=5000, random_state=42)
param_dist['logistic_regression'] = {
    'C': [1],
    'penalty': ['l2']
}

# LightGBM (if installed)
if importlib.util.find_spec('lightgbm'):
    from lightgbm import LGBMClassifier
    models['lightgbm'] = LGBMClassifier(random_state=42)
    param_dist['lightgbm'] = {
        'n_estimators': [100, 200, 300],
        'learning_rate': [0.01, 0.05, 0.1],
        'num_leaves': [31, 63, 127]
    }

# ------------------- Hyperparameter tuning -------------------
best_estimators = {}
for name, estimator in models.items():
    rs = RandomizedSearchCV(
        estimator,
        param_distributions=param_dist[name],
        n_iter=1,
        cv=2,
        scoring='f1_macro',
        random_state=42,
        n_jobs=-1)
    rs.fit(X_train_res, y_train_res)
    best_estimators[name] = rs.best_estimator_

# ------------------- Model selection (Fraud‑centric) -------------------
fraud_idx = label_encoder.transform(['Fraud'])[0]
validation_metrics = {}
for name, model in best_estimators.items():
    y_pred = model.predict(X_val_processed)
    recall = recall_score(y_val, y_pred, labels=[fraud_idx], average='macro')
    precision = precision_score(y_val, y_pred, labels=[fraud_idx], average='macro')
    f1 = f1_score(y_val, y_pred, labels=[fraud_idx], average='macro')
    cm = confusion_matrix(y_val, y_pred)
    false_neg = cm[fraud_idx, :].sum() - cm[fraud_idx, fraud_idx]
    roc_auc = roc_auc_score(y_val, model.predict_proba(X_val_processed), multi_class='ovr', average='weighted')
    validation_metrics[name] = {
        'recall': recall,
        'false_negatives': false_neg,
        'precision': precision,
        'f1': f1,
        'roc_auc': roc_auc
    }

# Sort according to required priority
sorted_models = sorted(
    validation_metrics.items(),
    key=lambda kv: (
        -kv[1]['recall'],          # highest recall
        kv[1]['false_negatives'],   # lowest false negatives
        -kv[1]['precision'],        # highest precision
        -kv[1]['f1'],               # highest f1
        -kv[1]['roc_auc']           # highest ROC‑AUC
    ))
selected_name = sorted_models[0][0]
selected_model = best_estimators[selected_name]

# ------------------- Evaluate on held-out test set -------------------
y_test_pred = selected_model.predict(X_test_processed)
test_recall = recall_score(y_test, y_test_pred, labels=[fraud_idx], average='macro')
test_precision = precision_score(y_test, y_test_pred, labels=[fraud_idx], average='macro')
test_f1 = f1_score(y_test, y_test_pred, labels=[fraud_idx], average='macro')
test_cm = confusion_matrix(y_test, y_test_pred)
test_false_neg = test_cm[fraud_idx, :].sum() - test_cm[fraud_idx, fraud_idx]
test_false_pos = test_cm[:, fraud_idx].sum() - test_cm[fraud_idx, fraud_idx]
test_roc_auc = roc_auc_score(y_test, selected_model.predict_proba(X_test_processed), multi_class='ovr', average='weighted')
# Save test metrics for later reporting
test_metrics = {
    'recall': test_recall,
    'precision': test_precision,
    'f1': test_f1,
    'roc_auc': test_roc_auc,
    'confusion_matrix': test_cm.tolist(),
    'false_negative_rate': test_false_neg / test_cm[fraud_idx, :].sum() if test_cm[fraud_idx, :].sum() > 0 else 0,
    'false_positive_rate': test_false_pos / test_cm[:, fraud_idx].sum() if test_cm[:, fraud_idx].sum() > 0 else 0
}
# Classification report for test set
test_report = classification_report(y_test, y_test_pred, target_names=label_encoder.classes_, output_dict=True)
# ------------------- Save model and metadata -------------------
output_dir = MODEL_DIR
os.makedirs(output_dir, exist_ok=True)
model_path = os.path.join(output_dir, 'fraud_model.pkl')
joblib.dump(selected_model, model_path)
# Save metadata JSON including test metrics
metadata = {
    'selected_model': selected_name,
    'training_timestamp': datetime.datetime.now().isoformat(),
    'label_classes': list(label_encoder.classes_),
    'test_metrics': test_metrics,
    'classification_report': test_report
}
with open(os.path.join(output_dir, 'model_metadata.json'), 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"Selected model: {selected_name}")
print(f"Model saved to {model_path}")
