import streamlit as st
from finance_manager import FinanceManager

st.set_page_config(page_title="FloosAfandy - إدارة الميزانيات", layout="wide", initial_sidebar_state="collapsed")

st.title("💼 إدارة الميزانيات")

fm = FinanceManager()

# Apply sidebar styles
def apply_sidebar_styles():
    st.markdown("""
        <style>
        .sidebar .sidebar-content {
            background-color: #f0f0f0;
            padding: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

apply_sidebar_styles()

# Horizontal navigation bar
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
with col1:
    if st.button("🏠 الرئيسية", key="nav_home"):
        st.switch_page("app.py")
with col2:
    if st.button("📊 لوحة التحكم", key="nav_dashboard"):
        st.switch_page("pages/dashboard.py")
with col3:
    if st.button("💳 المعاملات", key="nav_transactions"):
        st.switch_page("pages/transactions.py")
with col4:
    if st.button("🏦 الحسابات", key="nav_accounts"):
        st.switch_page("pages/accounts.py")
with col5:
    if st.button("💰 الميزانيات", key="nav_budgets"):
        st.switch_page("pages/budgets.py")
with col6:
    if st.button("📈 التقارير", key="nav_reports"):
        st.switch_page("pages/reports.py")
with col7:
    if st.button("📚 التعليمات", key="nav_instructions"):
        st.switch_page("pages/instructions.py")

# إضافة ميزانية جديدة
st.header("➕ إضافة ميزانية جديدة")
accounts = fm.get_all_accounts()
account_options = {acc[0]: acc[1] for acc in accounts}
account_id = st.selectbox("🏦 اختر الحساب", options=list(account_options.keys()), 
                          format_func=lambda x: account_options[x])
category = st.text_input("الفئة", placeholder="مثال: طعام، ترفيه")
budget_amount = st.number_input("المبلغ المخصص", min_value=0.0, step=100.0)
if st.button("إضافة الميزانية"):
    fm.add_budget(category, budget_amount, account_id)
    st.success(f"✅ تم إضافة ميزانية لـ {category} في حساب {account_options[account_id]}")

# عرض الميزانيات الحالية
st.header("📋 الميزانيات الحالية")
budgets = fm.get_budgets()
if budgets:
    for budget in budgets:
        account_name = account_options[budget[4]]
        st.write(f"**{account_name} - {budget[1]}**: مخصص {budget[2]:,.2f} | منفق {budget[3]:,.2f}")
        if budget[3] > budget[2]:
            st.warning(f"⚠️ تجاوزت الميزانية لـ {budget[1]} في حساب {account_name}")
else:
    st.info("ℹ️ لا توجد ميزانيات بعد")