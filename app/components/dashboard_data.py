# components/dashboard_data.py

from pathlib import Path
import pandas as pd
import json


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "simulations.csv"

MODEL_METADATA = PROJECT_ROOT / "data" / "trained_model" / "model_metadata.json"


def load_simulation_data():
    """
    Loads simulation history.
    Returns empty dataframe if file doesn't exist.
    """

    if DATA_PATH.exists():
        return pd.read_csv(DATA_PATH)

    return pd.DataFrame()


def load_model_metadata():

    if MODEL_METADATA.exists():

        with open(MODEL_METADATA, "r") as f:
            return json.load(f)

    return {}


def get_dashboard_metrics():

    df = load_simulation_data()
    metadata = load_model_metadata()

    metrics = {}

    metrics["total_transactions"] = len(df)

    if len(df):

        metrics["fraud_transactions"] = len(
            df[df["risk"] == "Fraud"]
        )

        metrics["legitimate_transactions"] = len(
            df[df["risk"] == "Legitimate"]
        )

        metrics["suspicious_transactions"] = len(
            df[df["risk"] == "Suspicious"]
        )

        metrics["fraud_rate"] = round(
            metrics["fraud_transactions"]
            / metrics["total_transactions"] * 100,
            2,
        )

        if "prob_fraud" in df.columns:

            metrics["avg_risk"] = round(
                df["prob_fraud"].mean() * 100,
                2,
            )

            metrics["high_risk_alerts"] = len(
                df[df["prob_fraud"] >= 0.80]
            )

        else:

            metrics["avg_risk"] = 0
            metrics["high_risk_alerts"] = 0

    else:

        metrics["fraud_transactions"] = 0
        metrics["legitimate_transactions"] = 0
        metrics["suspicious_transactions"] = 0
        metrics["fraud_rate"] = 0
        metrics["avg_risk"] = 0
        metrics["high_risk_alerts"] = 0

    test_metrics = metadata.get("test_metrics", {})

    metrics["model_precision"] = round(
        test_metrics.get("precision", 0) * 100,
        2,
    )

    metrics["model_recall"] = round(
        test_metrics.get("recall", 0) * 100,
        2,
    )

    metrics["model_f1"] = round(
        test_metrics.get("f1", 0) * 100,
        2,
    )

    metrics["model_auc"] = round(
        test_metrics.get("roc_auc", 0) * 100,
        2,
    )

    metrics["selected_model"] = metadata.get(
        "selected_model",
        "Unknown",
    )

    metrics["training_time"] = metadata.get(
        "training_timestamp",
        "Unknown",
    )

    return metrics, df