from pathlib import Path
import csv
import joblib
import pandas as pd
import sklearn
from packaging import version
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline

# Project root (two levels up)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / 'data' / 'datasets'
MODEL_DIR = PROJECT_ROOT / 'data' / 'trained_model'
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Load transactions data using csv
TRANSACTIONS_FILE = DATA_DIR / 'payment_transactions.csv'
if not TRANSACTIONS_FILE.is_file():
    raise FileNotFoundError(f'Could not find {TRANSACTIONS_FILE}')

rows = []
with open(TRANSACTIONS_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rows.append(row)

if not rows:
    raise ValueError('No data found in CSV file')

# Extract column names
columns = rows[0].keys()
IDENTIFIER_COLS = [

    # IDs
    'Transaction_ID',
    'User_ID',
    'Merchant_ID',
    'Device_ID',
    'Card_Number',
    'IP_Address',
    'Session_ID',

    # Personal identifiers
    'Customer_Name',
    'Phone_Number',
    'Email',
    'Account_Number',
    'UPI_ID',

    # Leakage columns
    'Fraud_Reason',
    'Risk_Score',
    'Confidence_Score',
    'Transaction_Status',

    # Derived leakage features
    'Amount_Category',
    'Is_High_Value',
    'Amount_vs_Average',
    'Merchant_High_Risk',
    'Merchant_Rating_Category',
    'IPAddress',

]
TARGET_COL = 'Fraud_Label'
if TARGET_COL not in columns:
    raise KeyError(f"Target column '{TARGET_COL}' not found in CSV")
# Separate features and target, excluding identifiers
X_raw = []
y_raw = []
for row in rows:
    y_raw.append(row[TARGET_COL])
    X_raw.append([value for key, value in row.items() if key != TARGET_COL and key not in IDENTIFIER_COLS])

# Encode target labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y_raw)

# Determine categorical vs numeric columns (simple heuristic: try float conversion)
num_indices = []
cat_indices = []
for idx in range(len(X_raw[0])):
    try:
        float(X_raw[0][idx])
        num_indices.append(idx)
    except ValueError:
        cat_indices.append(idx)

# Convert to numpy array (object dtype for categorical)

# Choose appropriate OneHotEncoder parameter based on scikit-learn version
if version.parse(sklearn.__version__) >= version.parse('1.2'):
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse_output=True)
else:
    categorical_transformer = OneHotEncoder(handle_unknown='ignore', sparse=True)



numeric_transformer = StandardScaler()
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', categorical_transformer, cat_indices),
        ('num', numeric_transformer, num_indices)
    ],
    remainder='drop'
)
pipeline = Pipeline(
    steps=[
        ('preprocess', preprocessor)
    ]
)

# Fit preprocessing pipeline
X_df = pd.DataFrame(
    X_raw,
    columns=[
        key for key in rows[0].keys()
        if key != TARGET_COL and key not in IDENTIFIER_COLS
    ]
)

pipeline.fit(X_df)

# Save fitted preprocessing pipeline
joblib.dump(
    pipeline,
    MODEL_DIR / 'preprocess.pkl'
)
joblib.dump(label_encoder, MODEL_DIR / 'label_encoder.pkl')
joblib.dump(y_encoded, MODEL_DIR / 'y_encoded.pkl')

print('Preprocessing completed successfully. Artifacts saved to:', MODEL_DIR)
