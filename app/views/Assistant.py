# =============================================================
# PayGuard AI
# Assistant
# Part 1 - Imports, Theme, Header & Session State
# =============================================================

import random

import streamlit as st

from components.theme import apply_theme

from components.assistant_engine import (
    ask_payguard_ai,
    format_context,
    engine_status,
)

# =============================================================
# Apply Theme
# =============================================================

apply_theme()

# =============================================================
# Load Assistant Information
# =============================================================

assistant_context = format_context()

assistant_status = engine_status()

# =============================================================
# Session State
# =============================================================

if "messages" not in st.session_state:

    st.session_state.messages = []

if "selected_question" not in st.session_state:

    st.session_state.selected_question = None

# =============================================================
# Page Header
# =============================================================

st.markdown(
    """
<div class="glass-card">

<h1 style="text-align:center;">
🤖 PayGuard AI Assistant
</h1>

<p style="
text-align:center;
font-size:18px;
color:#CBD5E1;
">

Your intelligent fraud investigation assistant.

Ask questions about PayGuard AI, fraud detection,
reports, dashboard, search, simulation or
transaction history.

</p>

</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# =============================================================
# Welcome Message
# =============================================================

st.success(
    """
### 👋 Welcome to PayGuard AI Assistant

I can help you with:

- 📊 Dashboard Analytics
- 🛡 Fraud Detection
- 💳 Transaction Investigation
- 📈 Reports & Insights
- 🔍 Search & Filtering
- 🤖 Machine Learning Predictions

❌ I only answer questions related to the PayGuard AI application.
"""
)

st.write("")
# =============================================================
# PART 2 - Suggested Questions
# =============================================================

st.subheader("💡 Suggested Questions")

st.caption(
    "Click any question below to instantly ask the PayGuard AI Assistant."
)

# -------------------------------------------------------------
# Question Bank
# -------------------------------------------------------------

QUESTION_BANK = [

    "📊 How many fraud transactions are there?",

    "📈 What is the current fraud rate?",

    "🚨 Show the highest fraud probability transaction.",

    "🏙️ Which city has the most fraud transactions?",

    "🏪 Which merchant category appears most frequently?",

    "💳 Which payment method is used the most?",

    "📄 Summarize the prediction history.",

    "🔍 Explain the latest transaction.",

    "🤖 Explain how the fraud prediction model works.",

    "⚠️ What is the difference between Fraud and Suspicious?",

    "📈 How many legitimate transactions are there?",

    "💰 What is the highest transaction amount?",

    "📍 Which city has the most transactions?",

    "📱 Which device is used the most?",

    "🌐 Which browser appears most frequently?",

    "🤖 What can this AI Assistant do?",

]

# -------------------------------------------------------------
# Random Suggestions
# -------------------------------------------------------------

display_questions = random.sample(

    QUESTION_BANK,

    min(10, len(QUESTION_BANK))

)

# -------------------------------------------------------------
# Display Buttons
# -------------------------------------------------------------

left, right = st.columns(2)

for index, question in enumerate(display_questions):

    target = left if index % 2 == 0 else right

    with target:

        if st.button(

            question,

            key=f"suggestion_{index}",

            width="stretch",

        ):

            st.session_state.selected_question = question

st.write("")
st.divider()
st.write("")
# =============================================================
# PART 3 - Quick Overview
# =============================================================

st.subheader("📊 Quick Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric(

        "Transactions",

        assistant_context["total_transactions"],

    )

with col2:

    st.metric(

        "Fraud",

        assistant_context["fraud_transactions"],

    )

with col3:

    st.metric(

        "Suspicious",

        assistant_context["suspicious_transactions"],

    )

with col4:

    st.metric(

        "Legitimate",

        assistant_context["legitimate_transactions"],

    )

with col5:

    st.metric(

        "Fraud Rate",

        f"{assistant_context['fraud_rate']}%",

    )

# -------------------------------------------------------------
# Latest Transaction Summary
# -------------------------------------------------------------

latest = assistant_context.get("latest_transaction")

if latest:

    st.info(
        f"""
### 📝 Latest Transaction

**Amount:** ₹{latest.get('amount', 'N/A')}

**City:** {latest.get('city', 'N/A')}

**Merchant:** {latest.get('merchant_category', 'N/A')}

**Prediction:** {latest.get('risk', 'N/A')}
"""
    )

st.write("")
st.divider()
st.write("")
# =============================================================
# PART 4 - AI Conversation
# =============================================================

st.subheader("💬 Conversation")

# -------------------------------------------------------------
# Handle Suggested Question
# -------------------------------------------------------------

if st.session_state.selected_question:

    question = st.session_state.selected_question

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.spinner("🤖 PayGuard AI is thinking..."):

        answer = ask_payguard_ai(
            question=question,
            conversation_history=st.session_state.messages,
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    st.session_state.selected_question = None

    st.rerun()

# -------------------------------------------------------------
# Display Conversation
# -------------------------------------------------------------

if not st.session_state.messages:

    st.info(
        """
👋 Start by clicking one of the suggested questions above
or ask your own PayGuard AI related question below.
"""
    )

else:

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
<div class="glass-card">

<b>👤 You</b>

<br>

{message["content"]}

</div>
""",
                unsafe_allow_html=True,
            )

        else:

            st.markdown(
                f"""
<div class="glass-card">

<b>🤖 PayGuard AI</b>

<br>

{message["content"]}

</div>
""",
                unsafe_allow_html=True,
            )

st.write("")
st.write("")
# =============================================================
# PART 5 - Ask Questions
# =============================================================

st.subheader("✍️ Ask Your Question")

col1, col2 = st.columns([6, 1])

with col1:

    user_question = st.text_input(

        "Ask your PayGuard AI question",

        placeholder="Ask about fraud, transactions, reports...",

        label_visibility="collapsed",

    )

with col2:

    send = st.button(

        "Send",

        width="stretch",

    )

# -------------------------------------------------------------
# Process User Question
# -------------------------------------------------------------

if send and user_question.strip():

    st.session_state.messages.append(

        {

            "role": "user",

            "content": user_question,

        }

    )

    with st.spinner("🤖 Analysing your question..."):

        answer = ask_payguard_ai(

            question=user_question,

            conversation_history=st.session_state.messages,

        )

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": answer,

        }

    )

    st.rerun()

st.write("")
st.divider()

# =============================================================
# PART 6 - Assistant Tools
# =============================================================

st.subheader("🛠 Assistant Tools")

tool1, tool2, tool3 = st.columns(3)

# -------------------------------------------------------------
# Clear Chat
# -------------------------------------------------------------

with tool1:

    if st.button(

        "🗑 Clear Conversation",

        width="stretch",

    ):

        st.session_state.messages = []

        st.session_state.selected_question = None

        st.rerun()

# -------------------------------------------------------------
# Download Chat
# -------------------------------------------------------------

with tool2:

    conversation = ""

    for message in st.session_state.messages:

        role = "You" if message["role"] == "user" else "PayGuard AI"

        conversation += f"{role}: {message['content']}\n\n"

    st.download_button(

        "💾 Download Chat",

        data=conversation,

        file_name="PayGuard_AI_Conversation.txt",

        mime="text/plain",

        width="stretch",

    )

# -------------------------------------------------------------
# Engine Status
# -------------------------------------------------------------

with tool3:

    if assistant_status["api_key_loaded"]:

        st.success("🟢 AI Online")

    else:

        st.error("🔴 AI Offline")

st.write("")
st.divider()

# =============================================================
# Footer
# =============================================================

st.caption(
    """
© 2026 PayGuard AI

The assistant answers only questions related to the PayGuard AI
application, fraud detection, reports, dashboard, search,
simulation and transaction investigation.
"""
)