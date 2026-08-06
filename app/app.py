# =============================================================
# PayGuard AI
# Main Application Entry
# =============================================================

import os
import sys
import importlib

import streamlit as st

# =============================================================
# Configure Python Paths
# =============================================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

APP_ROOT = os.path.abspath(
    os.path.dirname(__file__)
)

sys.path.append(PROJECT_ROOT)
sys.path.append(APP_ROOT)

# =============================================================
# Streamlit Configuration
# =============================================================

st.set_page_config(

    page_title="PayGuard AI",

    page_icon="🛡️",

    layout="wide",

    initial_sidebar_state="expanded",

)

# =============================================================
# Page Mapping
# =============================================================

PAGES = {

    "Landing": "views.Landing",

    "Dashboard": "views.Dashboard",

    "Simulation": "views.Simulation",

    "Search": "views.Search",

    "Reports": "views.Reports",

    "Assistant": "views.Assistant",

    "Profile": "views.Profile",

}

# =============================================================
# Dynamic Page Loader
# =============================================================

def load_page(page_name):

    module_name = PAGES[page_name]

    if module_name in sys.modules:

        importlib.reload(sys.modules[module_name])

    else:

        importlib.import_module(module_name)

# =============================================================
# Session State Navigation
# =============================================================

if "_navigate" not in st.session_state:

    st.session_state["_navigate"] = "Landing"

current_page = st.session_state["_navigate"]

# =============================================================
# Landing Page
# =============================================================

if current_page == "Landing":

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"]{
            display:none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# =============================================================
# Application Sidebar
# =============================================================

else:

    st.sidebar.markdown("# 🛡️ PayGuard AI")

    st.sidebar.caption(
        "AI Powered Fraud Detection Platform"
    )

    st.sidebar.divider()

    menu = [

        "Dashboard",

        "Simulation",

        "Search",

        "Reports",

        "Assistant",

        "Profile",

    ]

    if current_page not in menu:

        current_page = "Dashboard"

    selected = st.sidebar.radio(

        "Navigate",

        menu,

        index=menu.index(current_page),

        label_visibility="collapsed",

    )

    st.session_state["_navigate"] = selected

# =============================================================
# Load Selected Page
# =============================================================

load_page(
    st.session_state["_navigate"]
)