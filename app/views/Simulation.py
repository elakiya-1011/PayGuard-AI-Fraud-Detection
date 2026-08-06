# ============================================================
# PayGuard AI
# Transaction Simulation
# Part 1
# Imports • Theme • Model Loading • Utilities
# ============================================================

import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime

from components.theme import apply_theme

# ------------------------------------------------------------
# Apply Global Theme
# ------------------------------------------------------------

apply_theme()

# ------------------------------------------------------------
# Colors
# ------------------------------------------------------------

PRIMARY_COLOR = "#3B82F6"
SECONDARY_COLOR = "#8B5CF6"
SUCCESS_COLOR = "#10B981"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#EF4444"

# ------------------------------------------------------------
# Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"

DATASET_PATH = DATA_DIR / "datasets" / "payment_transactions.csv"

MODEL_DIR = DATA_DIR / "trained_model"

SIMULATION_CSV = DATA_DIR / "simulations.csv"

# ------------------------------------------------------------
# Load ML Artifacts
# ------------------------------------------------------------

@st.cache_resource
def load_artifacts():

    model = joblib.load(
        MODEL_DIR / "fraud_model.pkl"
    )

    preprocess = joblib.load(
        MODEL_DIR / "preprocess.pkl"
    )

    label_encoder = joblib.load(
        MODEL_DIR / "label_encoder.pkl"
    )

    return model, preprocess, label_encoder


model, preprocess, label_encoder = load_artifacts()

# ------------------------------------------------------------
# Create Simulation History
# ------------------------------------------------------------

def create_history_file():

    if SIMULATION_CSV.exists():
        return

    history = pd.DataFrame(
        columns=[
            "timestamp",
            "amount",
            "merchant_category",
            "payment_method",
            "city",
            "device",
            "risk",
            "prob_fraud",
            "prob_legit",
        ]
    )

    history.to_csv(
        SIMULATION_CSV,
        index=False,
    )


create_history_file()

# ------------------------------------------------------------
# Save Prediction History
# ------------------------------------------------------------

def save_prediction(record):

    history = pd.read_csv(
        SIMULATION_CSV
    )

    history = pd.concat(
        [
            history,
            pd.DataFrame([record]),
        ],
        ignore_index=True,
    )

    history.to_csv(
        SIMULATION_CSV,
        index=False,
    )

# ------------------------------------------------------------
# Risk Level
# ------------------------------------------------------------

def get_risk_level(probability):

    if probability >= 0.80:
        return "Fraud"

    elif probability >= 0.50:
        return "Suspicious"

    return "Legitimate"

# ------------------------------------------------------------
# Load One Sample Transaction
# (Used as a template for prediction)
# ------------------------------------------------------------

@st.cache_data
def load_sample_transaction():

    df = pd.read_csv(DATASET_PATH)

    return df.iloc[0].copy()
# ============================================================
# PAGE HEADER
# ============================================================

st.markdown(
    """
<div class="glass-card">

<h1 style="text-align:center;">
🛡️ Transaction Fraud Simulation
</h1>

<p style="text-align:center;font-size:18px;">
Enter transaction details and let the trained Machine Learning
model predict whether the transaction is
<b>Legitimate</b>, <b>Suspicious</b>, or <b>Fraud</b>.
</p>

</div>
""",
    unsafe_allow_html=True,
)

st.write("")
st.write("")

# ============================================================
# TRANSACTION INPUT FORM
# ============================================================

with st.form("prediction_form"):

    st.subheader("💳 Transaction Information")

    left, right = st.columns(2)

    # ========================================================
    # LEFT COLUMN
    # ========================================================

    with left:

        amount = st.number_input(
            "Transaction Amount (₹)",
            min_value=1.0,
            value=500.0,
            step=100.0,
        )

        merchant_category = st.selectbox(
            "Merchant Category",
            [
                "Finance",
                "Grocery",
                "Education",
                "Entertainment",
                "E-Commerce",
                "Healthcare",
                "Restaurant",
                "Travel",
                "Utilities",
            ],
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "UPI",
                "Credit Card",
                "Debit Card",
                "Wallet",
                "Net Banking",
            ],
        )

        device = st.selectbox(
            "Device",
            [
                "Android",
                "iPhone",
                "Windows Laptop",
                "MacBook",
                "Tablet",
            ],
        )

        browser = st.selectbox(
            "Browser",
            [
                "Chrome",
                "Edge",
                "Firefox",
                "Safari",
            ],
        )

    # ========================================================
    # RIGHT COLUMN
    # ========================================================

    with right:

        city = st.selectbox(
            "City",
            [
                "Ahmedabad",
                "Bangalore",
                "Chennai",
                "Delhi",
                "Hyderabad",
                "Jaipur",
                "Kochi",
                "Kolkata",
                "Mumbai",
            ],
        )

        age = st.slider(
            "Customer Age",
            18,
            80,
            30,
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
            ],
        )

        international = st.toggle(
            "International Transaction",
            value=False,
        )

    st.write("")
    st.write("")

    predict_button = st.form_submit_button(
        "🚀 Predict Fraud",
        width="stretch",
    )
# ============================================================
# PART 3
# Build Complete Model Input
# ============================================================

if predict_button:

    # --------------------------------------------------------
    # Load one template transaction from dataset
    # --------------------------------------------------------

    transaction = load_sample_transaction()

    # --------------------------------------------------------
    # Replace values entered by user
    # --------------------------------------------------------

    transaction["Age"] = age
    transaction["Gender"] = gender
    transaction["City"] = city

    transaction["Amount"] = amount
    transaction["Merchant_Category"] = merchant_category
    transaction["Payment_Method"] = payment_method

    transaction["Device"] = device
    transaction["Browser"] = browser

    # --------------------------------------------------------
    # Automatically generate remaining features
    # --------------------------------------------------------

    transaction["Occupation"] = "Software Engineer"

    state_mapping = {
        "Ahmedabad": "Gujarat",
        "Bangalore": "Karnataka",
        "Chennai": "Tamil Nadu",
        "Delhi": "Delhi",
        "Hyderabad": "Telangana",
        "Jaipur": "Rajasthan",
        "Kochi": "Kerala",
        "Kolkata": "West Bengal",
        "Mumbai": "Maharashtra",
    }

    transaction["State"] = state_mapping.get(city, "Tamil Nadu")

    transaction["Average_Spending"] = 5000

    transaction["Maximum_Spending"] = 25000

    transaction["Account_Age_Days"] = 1500

    transaction["Merchant_Rating"] = 4.5

    transaction["Transaction_Hour"] = datetime.now().hour

    weekday = datetime.now().strftime("%A")

    month = datetime.now().strftime("%B")

    transaction["Transaction_Day"] = weekday

    transaction["Transaction_Month"] = month

    transaction["Is_Weekend"] = weekday in ["Saturday", "Sunday"]

    transaction["Is_Night_Transaction"] = (
        transaction["Transaction_Hour"] >= 22
        or
        transaction["Transaction_Hour"] <= 5
    )

    if amount < 1000:
        transaction["Amount_Category"] = "Small"
    elif amount < 10000:
        transaction["Amount_Category"] = "Medium"
    else:
        transaction["Amount_Category"] = "Large"

    transaction["Is_High_Value"] = amount >= 10000

    transaction["Amount_vs_Average"] = (
        amount / transaction["Average_Spending"]
    )

    if merchant_category in [
        "Finance",
        "E-Commerce",
    ]:
        transaction["Merchant_Risk_Level"] = "High"
        transaction["Merchant_High_Risk"] = True
    elif merchant_category in [
        "Travel",
        "Entertainment",
    ]:
        transaction["Merchant_Risk_Level"] = "Medium"
        transaction["Merchant_High_Risk"] = False
    else:
        transaction["Merchant_Risk_Level"] = "Low"
        transaction["Merchant_High_Risk"] = False

    if device == "Android":

        transaction["Operating_System"] = "Android 14"

    elif device == "iPhone":

        transaction["Operating_System"] = "iOS 18"

    elif device == "MacBook":

        transaction["Operating_System"] = "macOS Sonoma"

    elif device == "Windows Laptop":

        transaction["Operating_System"] = "Windows 11"

    else:

        transaction["Operating_System"] = "Android Tablet"

    transaction["Network"] = "5G"

    transaction["Channel"] = (
        "Website"
        if device == "Windows Laptop"
        else "Mobile App"
    )

    transaction["Transaction_Status"] = "Completed"

    transaction["Merchant_Rating_Category"] = "Good"

    transaction["Risk_Score"] = 25

    transaction["Fraud_Reason"] = "Normal Transaction"

    transaction["Confidence_Score"] = 95

    # --------------------------------------------------------
    # Keep only model columns
    # --------------------------------------------------------

    model_columns = [

    "Transaction_Time",
    "Age",
    "Gender",
    "Occupation",
    "City",
    "State",
    "Average_Spending",
    "Maximum_Spending",
    "Account_Age_Days",
    "Merchant_Name",
    "Merchant_Category",
    "Merchant_Risk_Level",
    "Merchant_Rating",
    "Amount",
    "Payment_Method",
    "Device",
    "Browser",
    "Operating_System",
    "Network",
    "Channel",
    "Transaction_Hour",
    "Transaction_Day",
    "Transaction_Month",
    "Is_Weekend",
    "Is_Night_Transaction"

]

    input_df = pd.DataFrame(
    [{col: transaction[col] for col in model_columns}]
    )

    bool_columns = [
        "Is_Weekend",
        "Is_Night_Transaction"
    ]

    for col in bool_columns:
        if col in input_df.columns:
            input_df[col] = input_df[col].astype(str).str.title()


# ============================================================
# PART 4
# Prediction
# ============================================================

    try:

        # Preprocess input
        transformed = preprocess.transform(input_df)

        # Predict class
        prediction = model.predict(transformed)[0]

        # Predict probabilities
        probabilities = model.predict_proba(transformed)[0]

        # Convert numeric prediction to label
        predicted_label = label_encoder.inverse_transform(
            [prediction]
        )[0]

        # Probability lookup
        probability_dict = dict(
            zip(
                label_encoder.classes_,
                probabilities,
            )
        )

        fraud_probability = probability_dict.get(
            "Fraud",
            0.0,
        )

        legitimate_probability = probability_dict.get(
            "Legitimate",
            0.0,
        )

        suspicious_probability = probability_dict.get(
            "Suspicious",
            0.0,
        )

        risk = predicted_label

    except Exception as e:

        st.error(
            f"Prediction Failed\n\n{e}"
        )

        st.stop()
# ============================================================
# PART 5
# Save Prediction & Display Result
# ============================================================

    save_prediction(

        {
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "amount": amount,

            "merchant_category": merchant_category,

            "payment_method": payment_method,

            "city": city,

            "device": device,

            "risk": risk,

            "prob_fraud": round(
                fraud_probability,
                4,
            ),

            "prob_legit": round(
                legitimate_probability,
                4,
            ),
        }

    )

    st.write("")
    st.divider()

    st.success("Prediction Completed Successfully")

    st.subheader("Prediction Result")

    st.metric(
        "Risk Level",
        risk,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Fraud Probability",
            f"{fraud_probability:.2%}",
        )

    with col2:

        st.metric(
            "Legitimate Probability",
            f"{legitimate_probability:.2%}",
        )

    with col3:

        st.metric(
            "Suspicious Probability",
            f"{suspicious_probability:.2%}",
        )

    st.progress(
        float(fraud_probability)
    )

    st.info(
        f"Prediction generated using the trained "
        f"{type(model).__name__} model."
    )


    # ============================================================
    # PART 6
    # AI Recommendation & Transaction Summary
    # ============================================================

    st.write("")
    st.divider()


    # ------------------------------------------------------------
    # Recommendation
    # ------------------------------------------------------------

    if risk == "Fraud":

        st.error(
            """
### 🚨 AI Recommendation

This transaction has a **HIGH probability of fraud**.

Recommended actions:

• Block the transaction immediately

• Notify the customer

• Request identity verification

• Flag the account for investigation
"""
        )

    elif risk == "Suspicious":

        st.warning(
            """
### ⚠️ AI Recommendation

This transaction appears **Suspicious**.

Recommended actions:

• Verify customer identity

• Trigger OTP / MFA verification

• Monitor future transactions

• Allow only after confirmation
"""
        )

    else:

        st.success(
            """
### ✅ AI Recommendation

This transaction appears **Legitimate**.

Recommended actions:

• Allow transaction

• Continue monitoring normally

• No manual intervention required
"""
        )


    # ------------------------------------------------------------
    # Transaction Summary
    # ------------------------------------------------------------

    st.write("")
    st.subheader("📋 Transaction Summary")

    summary = pd.DataFrame({

        "Field": [

            "Amount",
            "City",
            "Merchant Category",
            "Payment Method",
            "Device",
            "Browser",
            "Customer Age",
            "Gender",
            "International",
            "Prediction",

        ],

        "Value": [

            f"₹ {amount:,.2f}",
            city,
            merchant_category,
            payment_method,
            device,
            browser,
            age,
            gender,
            "Yes" if international else "No",
            risk,

        ],

    })


    summary["Value"] = summary["Value"].astype(str)
    st.dataframe(

        summary,

        width="stretch",

        hide_index=True,

    )


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.caption(
    "Prediction generated using the trained Machine Learning model."
)

