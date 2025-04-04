import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import timedelta, datetime
from styles import apply_sidebar_styles

st.set_page_config(page_title="FloosAfandy - معاملات مؤقتة", layout="wide", initial_sidebar_state="collapsed")

# تهيئة الحالة
if "collapse_sidebar" not in st.session_state:
    st.session_state.collapse_sidebar = False
if "target_page" not in st.session_state:
    st.session_state.target_page = None

apply_sidebar_styles()

# Horizontal navigation bar
st.markdown("""
    <div class="horizontal-navbar">
        <img src="https://i.ibb.co/KpzDy27r/IMG-2998.png" alt="Logo">
    </div>
""", unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("🏠 الصفحة الرئيسية", key="nav_home_transactions_temp"):
        st.session_state.current_page = "home"
        st.rerun()
with col2:
    if st.button("💳 المعاملات", key="nav_transactions_transactions_temp"):
        st.session_state.current_page = "transactions"
        st.rerun()
with col3:
    if st.button("🏦 الحسابات", key="nav_accounts_transactions_temp"):
        st.session_state.current_page = "accounts"
        st.rerun()
with col4:
    if st.button("📊 التقارير", key="nav_reports_transactions_temp"):
        st.session_state.current_page = "reports"
        st.rerun()
with col5:
    if st.button("📚 التعليمات", key="nav_instructions_transactions_temp"):
        st.session_state.current_page = "instructions"
        st.rerun()

# التخزين المؤقت للبيانات
@st.cache_data
def get_all_transactions():
    fm = FinanceManager()
    return fm.get_all_transactions()

@st.cache_data
def get_all_accounts():
    fm = FinanceManager()
    return fm.get_all_accounts()

@st.cache_data
def get_custom_categories(account_id, trans_type):
    fm = FinanceManager()
    return fm.get_custom_categories(account_id, trans_type)

# Modify account retrieval logic
if "accounts" not in st.session_state:
    st.session_state.accounts = get_all_accounts()

# Display a progress bar while loading data
with st.spinner("جارٍ تحميل البيانات..."):
    accounts = st.session_state.accounts
    account_options = {acc[0]: acc[1] for acc in accounts}

# The rest of the code remains unchanged...
