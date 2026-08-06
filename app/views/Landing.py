# app/pages/Landing.py
"""
Landing Page for PayGuard AI
Public entry page (no authentication).
"""

import streamlit as st
from components.theme import apply_theme

apply_theme()
PRIMARY = "#2563EB"
SECONDARY = "#7C3AED"
BG = "#F4F8FF"



st.markdown("""
<div class="hero">
<h1>🛡️ PayGuard AI</h1>
<h3>AI-Powered Financial Fraud Detection Platform</h3>
<p>
PayGuard AI helps financial institutions identify fraudulent transactions
using Machine Learning and Explainable AI. The platform provides an
interactive dashboard, fraud simulation, intelligent search, AI assistant,
analytics reports, and project information through a clean, modern interface.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("## ✨ Features")

c1,c2,c3 = st.columns(3)

with c1:
    st.markdown("""
<div class="feature">
<h4>📊 Dashboard</h4>
View fraud statistics, KPIs and transaction insights.
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature">
<h4>🤖 AI Assistant</h4>
Ask questions about fraud detection using OpenRouter AI.
</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown("""
<div class="feature">
<h4>⚡ Fraud Simulation</h4>
Predict whether a transaction is fraudulent using the ML model.
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature">
<h4>📈 Reports</h4>
Generate charts and downloadable fraud reports.
</div>
""", unsafe_allow_html=True)

with c3:
    st.markdown("""
<div class="feature">
<h4>🔎 Smart Search</h4>
Search historical fraud records quickly.
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature">
<h4>👤 Profile</h4>
View project information and application details.
</div>
""", unsafe_allow_html=True)

st.write("")
left,center,right=st.columns([1,2,1])
with center:
    if st.button("🚀 Launch Application",width="stretch",type="primary"):
        st.session_state["_navigate"]="Dashboard"
        st.rerun()

st.markdown("""
<div class="footer">
<b>PayGuard AI</b><br>
Final Year Project • AI Powered FinTech Fraud Detection
</div>
""", unsafe_allow_html=True)