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
st.set_page_config(page_title="FloosAfandy", layout="centered", initial_sidebar_state=sidebar_state)

apply_sidebar_styles()

# التحقق من الانتقال إلى صفحة جديدة
if st.session_state.target_page:
    target = st.session_state.target_page
    st.session_state.target_page = None  # إعادة تعيين بعد الاستخدام
    st.session_state.collapse_sidebar = True  # التأكد من الإخفاء في الصفحة الجديدة
    st.switch_page(target)

with st.sidebar:
    st.image("IMG_2998.png", width=300)
    st.markdown("<h2>💰 FloosAfandy</h2>", unsafe_allow_html=True)
    fm = FinanceManager()
    alerts = fm.check_alerts()
    if alerts:
        st.markdown(f"<p style='text-align: center; color: #f1c40f;'>⚠️ {len(alerts)} تنبيهات</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>الصفحات</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 الرئيسية", key="nav_home"):
            st.session_state.target_page = "app.py"
            st.session_state.collapse_sidebar = True
            st.rerun()
    with col2:
        if st.button("💸 معاملاتي", key="nav_transactions"):
            st.session_state.target_page = "pages/transactions.py"
            st.session_state.collapse_sidebar = True
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        if st.button("🏦 حساباتي", key="nav_accounts"):
            st.session_state.target_page = "pages/accounts.py"
            st.session_state.collapse_sidebar = True
            st.rerun()
    with col4:
        if st.button("📊 تقاريري", key="nav_reports"):
            st.session_state.target_page = "pages/reports.py"
            st.session_state.collapse_sidebar = True
            st.rerun()

    col5, _ = st.columns([1, 1])
    with col5:
        if st.button("📈 لوحة التحكم", key="nav_dashboard"):
            st.session_state.target_page = "pages/dashboard.py"
            st.session_state.collapse_sidebar = True
            st.rerun()

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>الإعدادات</div>", unsafe_allow_html=True)
    with st.expander("⚙️ الفلاتر", expanded=False):
        accounts = fm.get_all_accounts()
        account_options = {acc[0]: acc[1] for acc in accounts}
        options_list = ["جميع الحسابات"] + list(account_options.keys())
        time_range = st.selectbox("⏳ الفترة", ["الكل", "آخر 7 أيام", "آخر 30 يومًا", "آخر 90 يومًا"], key="time_range")
        selected_account = st.selectbox("🏦 الحساب", options=options_list, 
                                        format_func=lambda x: "جميع الحسابات" if x == "جميع الحسابات" else account_options[x], 
                                        key="selected_account")
        if st.button("🔄 إعادة تعيين", key="reset_filters"):
            st.session_state.time_range = "الكل"
            st.session_state.selected_account = "جميع الحسابات"
            st.session_state.collapse_sidebar = False
            st.rerun()

# Main content

# Main content


st.title("📈 لوحة التحكم")
st.markdown("<p style='color: #6b7280;'>كل ما تحتاجه في نظرة واحدة</p>", unsafe_allow_html=True)
st.markdown("---")

fm = FinanceManager()
accounts = fm.get_all_accounts()
account_options = {acc[0]: acc[1] for acc in accounts}

# Filters
time_range = st.selectbox("⏳ الفترة الزمنية", ["الكل", "آخر 7 أيام", "آخر 30 يومًا", "آخر 90 يومًا"])
selected_account = st.selectbox("🏦 الحساب", ["جميع الحسابات"] + list(account_options.keys()), 
                                format_func=lambda x: "جميع الحسابات" if x == "جميع الحسابات" else account_options[x])

if time_range == "آخر 7 أيام":
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
elif time_range == "آخر 30 يومًا":
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
elif time_range == "آخر 90 يومًا":
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
else:
    start_date = None

transactions = fm.filter_transactions(account_id=selected_account if selected_account != "جميع الحسابات" else None, start_date=start_date)
df = pd.DataFrame(transactions, columns=["id", "date", "type", "amount", "account_id", "description", "payment_method", "category"]) if transactions else pd.DataFrame()

# Metrics
total_balance = sum(acc[2] for acc in accounts)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div style='background: linear-gradient(#34d399, #10b981); padding: 20px; border-radius: 10px; color: white;'>", unsafe_allow_html=True)
    st.metric("💰 إجمالي الرصيد", f"{total_balance:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='background: linear-gradient(#60a5fa, #3b82f6); padding: 20px; border-radius: 10px; color: white;'>", unsafe_allow_html=True)
    st.metric("📥 الوارد", f"{df[df['type'] == 'IN']['amount'].sum():,.2f}" if not df.empty else "0.00")
    st.markdown("</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='background: linear-gradient(#f87171, #ef4444); padding: 20px; border-radius: 10px; color: white;'>", unsafe_allow_html=True)
    st.metric("📤 الصادر", f"{df[df['type'] == 'OUT']['amount'].sum():,.2f}" if not df.empty else "0.00")
    st.markdown("</div>", unsafe_allow_html=True)

# Charts
if not df.empty:
    df["amount"] = pd.to_numeric(df["amount"], errors='coerce')
    df = df.dropna(subset=["amount"])
    df["date"] = pd.to_datetime(df["date"])
    chart_type = st.selectbox("📊 نوع الرسم البياني", ["خطي", "دائري", "شريطي"])
    if chart_type == "خطي":
        df["balance_change"] = df.apply(lambda x: x["amount"] if x["type"] == "IN" else -x["amount"], axis=1)
        balance_df = df[["date", "balance_change"]].sort_values("date")
        balance_df["cumulative_balance"] = balance_df["balance_change"].cumsum()
        fig = px.line(balance_df, x="date", y="cumulative_balance", title="تطور الرصيد", color_discrete_sequence=["#6b48ff"])
        st.plotly_chart(fig)
    elif chart_type == "دائري":
        fig = px.pie(values=[df[df["type"] == "IN"]["amount"].sum(), df[df["type"] == "OUT"]["amount"].sum()], 
                     names=["وارد", "صادر"], title="نسبة الوارد/الصادر", hole=0.3, color_discrete_map={"وارد": "#34d399", "صادر": "#f87171"})
        st.plotly_chart(fig)
    else:
        fig = px.bar(df, x="date", y="amount", color="type", title="المعاملات", color_discrete_map={"IN": "#34d399", "OUT": "#f87171"})
        st.plotly_chart(fig)

# Top Categories
st.subheader("📂 أعلى 5 فئات مصروفات")
if not df[df["type"] == "OUT"].empty:
    expenses_df = df[df["type"] == "OUT"].groupby("category")["amount"].sum().nlargest(5).reset_index()
    for i, row in expenses_df.iterrows():
        st.write(f"{'📤'} {row['category']}: {row['amount']:,.2f}")