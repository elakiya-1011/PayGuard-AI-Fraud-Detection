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

/* Streamlit Cloud dark background fix */

[data-testid="stAppViewContainer"]{
    background:#0B1120 !important;
}

[data-testid="stHeader"]{
    background:#0B1120 !important;
}

[data-testid="stToolbar"]{
    background:#0B1120 !important;
}


/* Main application */

.stApp{
    background:linear-gradient(180deg,#0B1120,#111827) !important;
}


.block-container{
    max-width:1200px;
    padding-top:2rem;
    padding-bottom:2rem;
}


/* Sidebar */

[data-testid="stSidebar"]{
    background:#111827 !important;
    border-right:1px solid rgba(255,255,255,.08);
}


[data-testid="stSidebar"] *{
    color:#E5E7EB !important;
}


/* Text styling */

h1,h2,h3,h4,h5,h6{
    color:#FFFFFF !important;
    font-family:Inter,sans-serif;
}


p,label,li,span{
    color:#CBD5E1 !important;
    font-family:Inter,sans-serif;
}


/* Glass card component */

.glass-card{
    background:rgba(30,41,59,.85);
    border:1px solid rgba(255,255,255,.08);
    border-radius:18px;
    padding:22px;
    box-shadow:0 10px 30px rgba(0,0,0,.25);
    backdrop-filter:blur(10px);
}


/* Buttons */

div.stButton > button{

    background:linear-gradient(90deg,#2563EB,#7C3AED);

    color:white !important;

    border:none;

    border-radius:12px;

    font-weight:700;

    padding:.7rem 1rem;

}


div.stButton > button:hover{
    filter:brightness(1.08);
}


/* Input fields */

.stTextInput input,
.stNumberInput input,
textarea{

    background:#1E293B !important;

    color:white !important;

    border:1px solid #334155 !important;

    border-radius:10px !important;

}


/* Selectbox dark theme fix */

div[data-baseweb="select"] > div{

    background:#1E293B !important;

    color:white !important;

    border-color:#334155 !important;

}


div[data-baseweb="select"] span{

    color:white !important;

}


ul[data-baseweb="menu"]{

    background:#1E293B !important;

}


li[data-baseweb="option"]{

    background:#1E293B !important;

    color:white !important;

}


li[data-baseweb="option"]:hover{

    background:#334155 !important;

}


/* Slider */

div[data-baseweb="slider"] *{

    color:white !important;

}


/* Metrics */

[data-testid="stMetric"]{

    background:#1E293B !important;

    border-radius:16px;

    padding:16px;

    border:1px solid rgba(255,255,255,.08);

}


/* Alerts */

[data-testid="stAlert"]{

    border-radius:12px;

}


/* Tables */

thead tr{

    background:#1E293B !important;

}


tbody tr{

    background:#111827 !important;

}


table *{

    color:#E5E7EB !important;

}


/* Hide Streamlit default UI */

footer{

    visibility:hidden;

}


#MainMenu{

    visibility:hidden;

}


</style>
""", unsafe_allow_html=True)