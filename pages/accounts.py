import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import timedelta, datetime
from styles import apply_sidebar_styles

# تعيين إعدادات الصفحة أولاً
st.set_page_config(page_title="FloosAfandy", layout="centered", initial_sidebar_state="auto")

# تهيئة الحالة
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "collapse_sidebar" not in st.session_state:
    st.session_state.collapse_sidebar = False
if "target_page" not in st.session_state:
    st.session_state.target_page = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

apply_sidebar_styles()

# التحقق من الانتقال إلى صفحة جديدة
if st.session_state.target_page:
    target = st.session_state.target_page
    st.session_state.target_page = None
    st.session_state.collapse_sidebar = True
    st.switch_page(target)

# التحقق من تسجيل الدخول
if "user_id" not in st.session_state or "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("يرجى تسجيل الدخول أولاً من الصفحة الرئيسية!")
    st.switch_page("app.py")
else:
    fm = FinanceManager(st.session_state.user_id)

    with st.sidebar:
        st.image("https://i.ibb.co/KpzDy27r/IMG-2998.png", width=300)
        st.markdown(f"<h2>💰 FloosAfandy - {st.session_state.user_id}</h2>", unsafe_allow_html=True)
        alerts = fm.check_alerts()
        if alerts:
            st.markdown(f"<p style='text-align: center; color: #f1c40f;'>⚠️ {len(alerts)} تنبيهات</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>الصفحات</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 الرئيسية", key="nav_home"):
                st.session_state.target_page = "app.py"
                st.rerun()
        with col2:
            if st.button("💸 معاملاتي", key="nav_transactions"):
                st.session_state.target_page = "pages/transactions.py"
                st.rerun()

        col3, col4 = st.columns(2)
        with col3:
            if st.button("🏦 حساباتي", key="nav_accounts"):
                st.session_state.target_page = "pages/accounts.py"
                st.rerun()
        with col4:
            if st.button("📊 تقاريري", key="nav_reports"):
                st.session_state.target_page = "pages/reports.py"
                st.rerun()

        if st.button("تسجيل الخروج", key="logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.rerun()

    st.title("🏦 حساباتي")
    st.markdown("<p style='color: #6b7280;'>تابع وأدر حساباتك المالية بسهولة</p>", unsafe_allow_html=True)
    st.markdown("---")

    accounts = fm.get_all_accounts()

    # Mobile-friendly CSS
    st.markdown("""
        <style>
        .card {background-color: #ffffff; padding: 10px; border-radius: 8px; margin: 5px 0; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
        @media (max-width: 768px) {
            .card {padding: 8px; font-size: 12px;}
            .stButton>button {font-size: 12px; padding: 6px;}
        }
        </style>
    """, unsafe_allow_html=True)

    # Statistics
    st.metric("عدد الحسابات", len(accounts))

    # Add Account Form
    st.subheader("➕ إضافة حساب جديد")
    with st.form(key="add_account_form"):
        account_name = st.text_input("🏦 اسم الحساب", key="add_name")
        opening_balance = st.number_input("💵 الرصيد الافتتاحي", min_value=0.0, step=0.01, format="%.2f", key="add_balance")
        min_balance = st.number_input("🚨 الحد الأدنى", min_value=0.0, step=0.01, format="%.2f", key="add_min")
        submit_button = st.form_submit_button("💾 إضافة الحساب", type="primary", use_container_width=True)
    if submit_button:
        fm.add_account(account_name, opening_balance, min_balance)
        st.success("✅ تم إضافة الحساب!")
        st.rerun()

    # Accounts as Cards
    st.subheader("📋 حساباتك")
    search_query = st.text_input("🔍 ابحث عن حساب", "")
    filtered_accounts = [acc for acc in accounts if search_query.lower() in acc[2].lower()] if search_query else accounts

    if filtered_accounts:
        for acc in filtered_accounts:
            bg_color = "#d1fae5" if acc[3] >= acc[4] else "#fee2e2"
            with st.container():
                st.markdown(f"<div class='card' style='background-color: {bg_color};'>"
                            f"<strong>{acc[2]}</strong><br>الرصيد: {acc[3]:,.2f}<br>الحد الأدنى: {acc[4]:,.2f}</div>", 
                            unsafe_allow_html=True)
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("📊 المعاملات", key=f"trans_{acc[0]}"):
                        st.session_state["filter_account"] = acc[0]
                        st.switch_page("pages/transactions.py")
                with col2:
                    if st.button("✏️ تعديل", key=f"edit_{acc[0]}"):
                        st.session_state[f"edit_{acc[0]}"] = True
                with col3:
                    if st.button("🗑️ حذف", key=f"del_{acc[0]}"):
                        fm.conn.execute("DELETE FROM accounts WHERE user_id = ? AND id = ?", (st.session_state.user_id, acc[0]))
                        fm.conn.commit()
                        st.success("🗑️ تم الحذف!")
                        st.rerun()
                if st.session_state.get(f"edit_{acc[0]}", False):
                    with st.form(key=f"edit_form_{acc[0]}"):
                        new_name = st.text_input("اسم جديد", value=acc[2], key=f"edit_name_{acc[0]}")
                        new_balance = st.number_input("الرصيد", value=float(acc[3]), key=f"edit_balance_{acc[0]}")
                        new_min = st.number_input("الحد الأدنى", value=float(acc[4]), key=f"edit_min_{acc[0]}")
                        if st.form_submit_button("💾 حفظ التعديل"):
                            fm.conn.execute("UPDATE accounts SET name = ?, balance = ?, min_balance = ? WHERE user_id = ? AND id = ?", 
                                            (new_name, new_balance, new_min, st.session_state.user_id, acc[0]))
                            fm.conn.commit()
                            st.success("✅ تم التعديل!")
                            st.session_state[f"edit_{acc[0]}"] = False
                            st.rerun()
    else:
        st.info("ℹ️ لا توجد حسابات تطابق البحث.")
