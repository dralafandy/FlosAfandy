import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import timedelta, datetime
from styles import apply_sidebar_styles

# تهيئة الحالة
if "collapse_sidebar" not in st.session_state:
    st.session_state.collapse_sidebar = False
if "target_page" not in st.session_state:
    st.session_state.target_page = None

# تحديد حالة القائمة الجانبية
sidebar_state = "collapsed" if st.session_state.collapse_sidebar else "expanded"
st.set_page_config(page_title="FloosAfandy - معاملاتي", layout="wide", initial_sidebar_state=sidebar_state)

apply_sidebar_styles()

# التحقق من الانتقال إلى صفحة جديدة
if st.session_state.target_page:
    target = st.session_state.target_page
    st.session_state.target_page = None
    st.session_state.collapse_sidebar = True
    st.switch_page(target)

# التخزين المؤقت للبيانات
@st.cache_data
def get_all_transactions():
    fm = FinanceManager()
    return fm.get_all_transactions()

# Remove the caching decorator
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

accounts = st.session_state.accounts
account_options = {acc[0]: acc[1] for acc in accounts}

# The rest of the code remains unchanged...
