PROJECT_NAME = "PayGuard AI"

VERSION = "1.0"

PRIMARY_COLOR = "#3B82F6"

SECONDARY_COLOR = "#8B5CF6"

SUCCESS_COLOR = "#10B981"

WARNING_COLOR = "#F59E0B"

DANGER_COLOR = "#EF4444"

COMPANY = "PayGuard AI"

COPYRIGHT = "© 2026 PayGuard AI"

MODEL_NAME = "Random Forest Fraud Detector"
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

DATASET_DIR = DATA_DIR / "datasets"

MODEL_DIR = DATA_DIR / "trained_model"

SIMULATION_CSV = DATA_DIR / "simulations.csv"

TRAINING_DATA = DATASET_DIR / "payment_transactions.csv"

MODEL_FILE = MODEL_DIR / "fraud_model.pkl"

PREPROCESS_FILE = MODEL_DIR / "preprocess.pkl"

LABEL_ENCODER_FILE = MODEL_DIR / "label_encoder.pkl"

MODEL_METADATA = MODEL_DIR / "model_metadata.json"