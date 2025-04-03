import streamlit as st
import pandas as pd
from finance_manager import FinanceManager
from datetime import timedelta, datetime
import plotly.express as px
from styles import apply_sidebar_styles

# تهيئة الحالة
if "collapse_sidebar" not in st.session_state:
    st.session_state.collapse_sidebar = False
if "target_page" not in st.session_state:
    st.session_state.target_page = None

# تحديد حالة القائمة الجانبية
sidebar_state = "collapsed" if st.session_state.collapse_sidebar else "expanded"
st.set_page_config(page_title="FloosAfandy - إحسبها يا عشوائي !!", layout="wide", initial_sidebar_state=sidebar_state)

apply_sidebar_styles()

# التحقق من الانتقال إلى صفحة جديدة
if st.session_state.target_page:
    target = st.session_state.target_page
    st.session_state.target_page = None
    st.session_state.collapse_sidebar = True
    st.switch_page(target)

# التخزين المؤقت للبيانات
@st.cache_data
def get_filtered_transactions(account_id, start_date):
    fm = FinanceManager()
    return fm.filter_transactions(account_id=account_id, start_date=start_date)

@st.cache_data
def get_all_accounts():
    fm = FinanceManager()
    return fm.get_all_accounts()

with st.sidebar:
    col_close, _ = st.columns([1, 5])
    with col_close:
        if st.button("✖", key="close_sidebar"):
            st.session_state.collapse_sidebar = True
            st.rerun()
    st.image("https://i.ibb.co/hxjbR4Hv/IMG-2998.png", width=300, use_container_width=True)
    st.markdown("<h2>💰 FloosAfandy</h2>", unsafe_allow_html=True)
    fm = FinanceManager()
    alerts = fm.check_alerts()
    if alerts:
        st.markdown(f"<p style='text-align: center; color: #f1c40f;'>⚠️ {len(alerts)} تنبيهات</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>الصفحات</div>", unsafe_allow_html=True)
    current_page = "app.py"  # لوحة التحكم هي الرئيسية
    
    col1, col2 = st.columns(2)
    with col1:
        btn_style = "background: linear-gradient(90deg, #B8E8EF, #A0E0DB);" if current_page == "app.py" else ""
        st.markdown(f"<style>#nav_dashboard {{ {btn_style} }}</style>", unsafe_allow_html=True)
        if st.button("📈 لوحة التحكم", key="nav_dashboard"):
            st.session_state.target_page = "app.py"
            st.session_state.collapse_sidebar = True
            st.rerun()
    with col2:
        btn_style = "background: linear-gradient(90deg, #B8E8EF, #A0E0DB);" if current_page == "pages/transactions.py" else ""
        st.markdown(f"<style>#nav_transactions {{ {btn_style} }}</style>", unsafe_allow_html=True)
        if st.button("💸 معاملاتي", key="nav_transactions"):
            st.session_state.target_page = "pages/transactions.py"
            st.session_state.collapse_sidebar = True
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        btn_style = "background: linear-gradient(90deg, #B8E8EF, #A0E0DB);" if current_page == "pages/accounts.py" else ""
        st.markdown(f"<style>#nav_accounts {{ {btn_style} }}</style>", unsafe_allow_html=True)
        if st.button("🏦 حساباتي", key="nav_accounts"):
            st.session_state.target_page = "pages/accounts.py"
            st.session_state.collapse_sidebar = True
            st.rerun()
    with col4:
        btn_style = "background: linear-gradient(90deg, #B8E8EF, #A0E0DB);" if current_page == "pages/reports.py" else ""
        st.markdown(f"<style>#nav_reports {{ {btn_style} }}</style>", unsafe_allow_html=True)
        if st.button("📊 تقاريري", key="nav_reports"):
            st.session_state.target_page = "pages/reports.py"
            st.session_state.collapse_sidebar = True
            st.rerun()
st.image("https://i.ibb.co/hxjbR4Hv/IMG-2998.png", width=300, use_container_width=True)
# Main content
st.markdown("<p style='text-align: center; color: #6b7280;'>إدارة مالياتك بسهولة وأناقة</p>", unsafe_allow_html=True)
st.markdown("---")

# Default button for "معاملة جديدة"
if st.button("➕ معاملة جديدة", key="new_transaction"):
    st.session_state.target_page = "pages/new_transaction.py"
    st.session_state.collapse_sidebar = True
    st.rerun()

# Buttons for each page in the main content
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
with col_btn1:
    if st.button("📈 لوحة التحكم", key="main_dashboard"):
        st.session_state.target_page = "app.py"
        st.session_state.collapse_sidebar = True
        st.rerun()
with col_btn2:
    if st.button("💸 معاملاتي", key="main_transactions"):
        st.session_state.target_page = "pages/transactions.py"
        st.session_state.collapse_sidebar = True
        st.rerun()
with col_btn3:
    if st.button("🏦 حساباتي", key="main_accounts"):
        st.session_state.target_page = "pages/accounts.py"
        st.session_state.collapse_sidebar = True
        st.rerun()
with col_btn4:
    if st.button("📊 تقاريري", key="main_reports"):
        st.session_state.target_page = "pages/reports.py"
        st.session_state.collapse_sidebar = True
        st.rerun()

# Filters
col_filter1, col_filter2, col_filter3 = st.columns([2, 2, 1])
with col_filter1:
    time_range = st.selectbox("⏳ الفترة الزمنية", ["الكل", "آخر 7 أيام", "آخر 30 يومًا", "آخر 90 يومًا"], key="time_range")
with col_filter2:
    accounts = get_all_accounts()
    account_options = {acc[0]: acc[1] for acc in accounts}
    selected_account = st.selectbox("🏦 الحساب", ["جميع الحسابات"] + list(account_options.keys()), 
                                    format_func=lambda x: "جميع الحسابات" if x == "جميع الحسابات" else account_options[x], key="selected_account")
with col_filter3:
    if st.button("🔄 إعادة تعيين", key="reset_filters"):
        st.session_state.time_range = "الكل"
        st.session_state.selected_account = "جميع الحسابات"
        st.rerun()

# حساب التواريخ
if time_range == "آخر 7 أيام":
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
elif time_range == "آخر 30 يومًا":
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
elif time_range == "آخر 90 يومًا":
    start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d %H:%M:%S")
else:
    start_date = None

# جلب البيانات
transactions = get_filtered_transactions(selected_account if selected_account != "جميع الحسابات" else None, start_date)
df = pd.DataFrame(transactions, columns=["id", "date", "type", "amount", "account_id", "description", "payment_method", "category"]) if transactions else pd.DataFrame()

# Alerts
if alerts:
    with st.expander("📢 تنبيهات مهمة", expanded=True):
        for alert in alerts:
            st.warning(alert)

# Metrics مع ألوان مخصصة
total_balance = sum(acc[2] for acc in accounts)
income = df[df["type"] == "IN"]["amount"].sum() if not df.empty else 0.00
expenses = df[df["type"] == "OUT"]["amount"].sum() if not df.empty else 0.00
net = income - expenses

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("<div style='background: linear-gradient(#d1d5db, #9ca3af); padding: 20px; border-radius: 10px; color: #1A2525;'>", unsafe_allow_html=True)
    st.metric("💰 إجمالي الرصيد", f"{total_balance:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='background: linear-gradient(#86efac, #22c55e); padding: 20px; border-radius: 10px; color: #1A2525;'>", unsafe_allow_html=True)
    st.metric("📥 الوارد", f"{income:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div style='background: linear-gradient(#f87171, #ef4444); padding: 20px; border-radius: 10px; color: #ffffff;'>", unsafe_allow_html=True)
    st.metric("📤 الصادر", f"{expenses:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)
with col4:
    st.markdown("<div style='background: linear-gradient(#60a5fa, #3b82f6); padding: 20px; border-radius: 10px; color: #ffffff;'>", unsafe_allow_html=True)
    st.metric("📊 الصافي", f"{net:,.2f}", delta=f"{net:,.2f}", delta_color="normal")
    st.markdown("</div>", unsafe_allow_html=True)

# Charts مع ألوان متسقة
if not df.empty:
    df["amount"] = pd.to_numeric(df["amount"], errors='coerce')
    df = df.dropna(subset=["amount"])
    df["date"] = pd.to_datetime(df["date"])

    st.markdown("<h3 style='color: #1A2525;'>تطور الرصيد</h3>", unsafe_allow_html=True)
    df["balance_change"] = df.apply(lambda x: x["amount"] if x["type"] == "IN" else -x["amount"], axis=1)
    balance_df = df[["date", "balance_change"]].sort_values("date")
    balance_df["cumulative_balance"] = balance_df["balance_change"].cumsum()
    fig_line = px.line(balance_df, x="date", y="cumulative_balance", title="", color_discrete_sequence=["#3b82f6"])  # أزرق للصافي
    st.plotly_chart(fig_line, use_container_width=True)

    chart_type = st.selectbox("📊 نوع الرسم البياني الإضافي", ["دائري", "شريطي"])
    if chart_type == "دائري":
        fig_pie = px.pie(values=[income, expenses], names=["وارد", "صادر"], title="نسبة الوارد/الصادر", hole=0.3, 
                         color_discrete_map={"وارد": "#22c55e", "صادر": "#ef4444"})  # أخضر وأحمر
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        fig_bar = px.bar(df, x="date", y="amount", color="type", title="المعاملات", 
                         color_discrete_map={"IN": "#22c55e", "OUT": "#ef4444"})  # أخضر وأحمر
        st.plotly_chart(fig_bar, use_container_width=True)

# Top Categories and Recent Transactions
col_cat, col_trans = st.columns(2)
with col_cat:
    st.markdown("<h3 style='color: #1A2525;'>أعلى 5 فئات مصروفات</h3>", unsafe_allow_html=True)
    if not df[df["type"] == "OUT"].empty:
        expenses_df = df[df["type"] == "OUT"].groupby("category")["amount"].sum().nlargest(5).reset_index()
        for i, row in expenses_df.iterrows():
            st.write(f"📤 {row['category']}: {row['amount']:,.2f}")
    else:
        st.write("لا توجد مصروفات.")
with col_trans:
    st.markdown("<h3 style='color: #1A2525;'>آخر 5 معاملات</h3>", unsafe_allow_html=True)
    if not df.empty:
        recent_df = df.sort_values("date", ascending=False).head(5)
        for i, row in recent_df.iterrows():
            icon = "📥" if row["type"] == "IN" else "📤"
            color = "#22c55e" if row["type"] == "IN" else "#ef4444"
            st.markdown(f"<span style='color: {color};'>{icon}</span> {row['date'].strftime('%Y-%m-%d')} - {row['description']}: {row['amount']:,.2f}", unsafe_allow_html=True)
    else:
        st.write("لا توجد معاملات حديثة.")