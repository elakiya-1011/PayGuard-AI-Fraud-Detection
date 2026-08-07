"""
Shared UI Theme for PayGuard AI
Import in every page:

from components.theme import apply_theme
apply_theme()
"""

import streamlit as st

def apply_theme():
    st.markdown("""
<style>
/* ---------- STREAMLIT CLOUD FIX ---------- */

[data-testid="stAppViewContainer"]{
    background:#0B1120;
}

[data-testid="stHeader"]{
    background:#0B1120;
}

[data-testid="stToolbar"]{
    background:#0B1120;
}

section[data-testid="stSidebar"]{
    background:#111827;
}


/* Fix dataframe background */

[data-testid="stDataFrame"]{
    background:#111827;
}


/* Fix charts container */

.element-container{
    background:transparent;
}

/* ---------- GLOBAL ---------- */

.stApp{
    background: linear-gradient(180deg,#0B1120,#111827);
}

.block-container{
    max-width:1200px;
    padding-top:2rem;
    padding-bottom:2rem;
}

/* ---------- SIDEBAR ---------- */

[data-testid="stSidebar"]{
    background:#111827;
    border-right:1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] *{
    color:#E5E7EB !important;
}

/* ---------- HEADINGS ---------- */

h1,h2,h3,h4,h5,h6{
    color:#FFFFFF !important;
    font-family:Inter,sans-serif;
}

p,label,li,span,div{
    color:#CBD5E1;
    font-family:Inter,sans-serif;
}

/* ---------- GLASS CARD ---------- */

.glass-card{
    background:rgba(30,41,59,.85);
    border:1px solid rgba(255,255,255,.08);
    border-radius:18px;
    padding:22px;
    box-shadow:0 10px 30px rgba(0,0,0,.25);
    backdrop-filter:blur(10px);
}

/* ---------- BUTTONS ---------- */

div.stButton>button{
    background:linear-gradient(90deg,#2563EB,#7C3AED);
    color:white !important;
    border:none;
    border-radius:12px;
    font-weight:700;
    padding:.7rem 1rem;
}

div.stButton>button:hover{
    filter:brightness(1.08);
}

/* ---------- INPUTS ---------- */

.stTextInput input,
.stNumberInput input,
textarea{
    background:#1E293B !important;
    color:white !important;
    border:1px solid #334155 !important;
    border-radius:10px !important;
}

.stSelectbox div[data-baseweb="select"]{
    background:#1E293B;
}

/* ---------- METRICS ---------- */

[data-testid="stMetric"]{
    background:#1E293B;
    border-radius:16px;
    padding:16px;
    border:1px solid rgba(255,255,255,.08);
}

/* ---------- ALERTS ---------- */

[data-testid="stAlert"]{
    border-radius:12px;
}

/* ---------- TABLES ---------- */

thead tr{
    background:#1E293B !important;
}

tbody tr{
    background:#111827 !important;
}

table *{
    color:#E5E7EB !important;
}

/* ---------- FOOTER ---------- */

footer{
    visibility:hidden;
}

/* ---------- MENU ---------- */

#MainMenu{
    visibility:hidden;
}

</style>
""", unsafe_allow_html=True)