# ============================================================
# PayGuard AI
# Security Analyst Profile
# ============================================================

import os
from pathlib import Path
import pandas as pd
import streamlit as st

from components.theme import apply_theme


# ------------------------------------------------------------
# Apply Theme
# ------------------------------------------------------------

apply_theme()


# ------------------------------------------------------------
# Project Paths
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "simulations.csv"


# ------------------------------------------------------------
# Load Prediction History
# ------------------------------------------------------------

@st.cache_data(ttl=5)
def load_history():

    if DATA_PATH.exists():

        return pd.read_csv(DATA_PATH)

    return pd.DataFrame()


history = load_history()


# ------------------------------------------------------------
# Page Header
# ------------------------------------------------------------

st.markdown(
    """
<div class="glass-card">

<h1 style="text-align:center;">
🛡️ PayGuard AI Analyst Profile
</h1>

<p style="text-align:center;
font-size:18px;
color:#CBD5E1;">

AI Powered Fraud Investigation Workspace

</p>

</div>
""",
    unsafe_allow_html=True,
)


st.write("")


# ------------------------------------------------------------
# Analyst Information
# ------------------------------------------------------------

col1, col2 = st.columns([1,4])


with col1:

    st.markdown(
        """
<div style="
font-size:70px;
text-align:center;
">
👨‍💻
</div>
""",
        unsafe_allow_html=True,
    )


with col2:

    st.subheader("Fraud Investigation Analyst")

    st.write(
        """
**User Type:** Security Analyst

**Role:** Fraud Detection Investigator

**Access Level:** Application Administrator

**Status:** Active
"""
    )


st.divider()


# ------------------------------------------------------------
# Live Analytics
# ------------------------------------------------------------

st.subheader("📊 Analyst Activity Overview")


if history.empty:

    total = 0
    fraud = 0
    suspicious = 0
    legitimate = 0

else:

    total = len(history)

    fraud = len(
        history[
            history["risk"] == "Fraud"
        ]
    )

    suspicious = len(
        history[
            history["risk"] == "Suspicious"
        ]
    )

    legitimate = len(
        history[
            history["risk"] == "Legitimate"
        ]
    )


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Predictions",
        total
    )


with col2:

    st.metric(
        "Fraud Detected",
        fraud
    )


with col3:

    st.metric(
        "Suspicious Cases",
        suspicious
    )


with col4:

    st.metric(
        "Legitimate",
        legitimate
    )


st.divider()


# ------------------------------------------------------------
# AI System Information
# ------------------------------------------------------------

st.subheader("🤖 AI System Information")


model_path = (
    PROJECT_ROOT /
    "trained_model"
)


system_info = {

    "AI Platform":
        "PayGuard AI",

    "Prediction Engine":
        "Machine Learning Fraud Classifier",

    "Model Storage":
        "trained_model/",

    "Model Status":
        "Loaded" if model_path.exists()
        else "Unavailable",

    "Data Source":
        "simulations.csv",

    "AI Assistant":
        "OpenRouter Powered",

}


for key, value in system_info.items():

    st.markdown(
        f"""
**{key}:**
{value}
"""
    )


st.divider()


# ------------------------------------------------------------
# Recent Investigation Activity
# ------------------------------------------------------------

st.subheader("📋 Recent Investigation Activity")


if history.empty:

    st.info(
        "No transaction investigations available."
    )

else:

    recent = history.tail(5).copy()

    display_columns = [

        "timestamp",
        "amount",
        "city",
        "merchant_category",
        "risk"

    ]

    existing_columns = [

        col
        for col in display_columns
        if col in recent.columns

    ]


    st.dataframe(

        recent[existing_columns],

        width="stretch",

        hide_index=True

    )


st.divider()


# ------------------------------------------------------------
# Platform Information
# ------------------------------------------------------------

st.subheader("⚙️ Platform Information")


platform = {

    "Application":
        "PayGuard AI Fraud Detection Platform",

    "Version":
        "1.0",

    "Environment":
        "Streamlit",

    "Prediction Storage":
        "CSV Based Transaction History",

    "Architecture":
        "Machine Learning + AI Assistant",

}


for key, value in platform.items():

    st.markdown(
        f"""
**{key}:**
{value}
"""
    )


# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.caption(
    "© 2026 PayGuard AI | Intelligent Fraud Detection Platform"
)