import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import datetime, timedelta
from mobile_styles import apply_mobile_styles

# تعيين إعدادات الصفحة
st.set_page_config(
    page_title="FloosAfandy - لوحة التحكم", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    page_icon="📊"
)

# تهيئة الحالة
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "collapse_sidebar" not in st.session_state:
    st.session_state.collapse_sidebar = False
if "target_page" not in st.session_state:
    st.session_state.target_page = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "language" not in st.session_state:
    st.session_state.language = "ar"  # Default to Arabic

apply_mobile_styles()

# دالة للترجمة
def translate(text, lang):
    translations = {
        "dashboard": {"ar": "لوحة التحكم", "en": "Dashboard"},
        "login_required": {"ar": "يرجى تسجيل الدخول أولاً من الصفحة الرئيسية!", "en": "Please login first from the home page!"},
        "welcome": {"ar": "مرحبًا بك في لوحة التحكم", "en": "Welcome to Dashboard"},
        "today": {"ar": "اليوم هو", "en": "Today is"},
        "overview": {"ar": "📊 نظرة عامة", "en": "📊 Overview"},
        "total_balance": {"ar": "💰 إجمالي الرصيد", "en": "💰 Total Balance"},
        "total_income": {"ar": "📥 إجمالي الوارد", "en": "📥 Total Income"},
        "total_expenses": {"ar": "📤 إجمالي المصروفات", "en": "📤 Total Expenses"},
        "net_balance": {"ar": "📊 صافي الرصيد", "en": "📊 Net Balance"},
        "no_accounts": {"ar": "ℹ️ لا توجد حسابات مسجلة.", "en": "ℹ️ No accounts registered."},
        "alerts": {"ar": "🚨 التنبيهات", "en": "🚨 Alerts"},
        "no_alerts": {"ar": "✅ لا توجد تنبيهات حالياً.", "en": "✅ No current alerts."},
        "analysis": {"ar": "📈 التحليل المالي", "en": "📈 Financial Analysis"},
        "insufficient_data": {"ar": "ℹ️ لا توجد بيانات كافية لعرض التحليل المالي.", "en": "ℹ️ Insufficient data for financial analysis."},
        "recent_activity": {"ar": "🕒 الأنشطة الأخيرة", "en": "🕒 Recent Activity"},
        "no_transactions": {"ar": "ℹ️ لا توجد معاملات مسجلة.", "en": "ℹ️ No transactions recorded."},
        "top_categories": {"ar": "📂 أعلى الفئات", "en": "📂 Top Categories"},
        "view_categories": {"ar": "عرض أعلى الفئات", "en": "View Top Categories"},
        "home": {"ar": "🏠 الرئيسية", "en": "🏠 Home"},
        "transactions": {"ar": "💳 المعاملات", "en": "💳 Transactions"},
        "accounts": {"ar": "🏦 الحسابات", "en": "🏦 Accounts"},
        "budgets": {"ar": "💰 الميزانيات", "en": "💰 Budgets"},
        "reports": {"ar": "📈 التقارير", "en": "📈 Reports"},
        "instructions": {"ar": "📚 التعليمات", "en": "📚 Instructions"},
        "currency": {"ar": "جنيه", "en": "EGP"}
    }
    
    if text in translations:
        return translations[text][lang]
    return text

# Horizontal navigation bar with language switcher
nav_cols = st.columns(8)
with nav_cols[0]:
    if st.button(translate("home", st.session_state.language), key="nav_home"):
        st.switch_page("app.py")
with nav_cols[1]:
    if st.button(translate("dashboard", st.session_state.language), key="nav_dashboard"):
        st.switch_page("pages/dashboard.py")
with nav_cols[2]:
    if st.button(translate("transactions", st.session_state.language), key="nav_transactions"):
        st.switch_page("pages/transactions.py")
with nav_cols[3]:
    if st.button(translate("accounts", st.session_state.language), key="nav_accounts"):
        st.switch_page("pages/accounts.py")
with nav_cols[4]:
    if st.button(translate("budgets", st.session_state.language), key="nav_budgets"):
        st.switch_page("pages/budgets.py")
with nav_cols[5]:
    if st.button(translate("reports", st.session_state.language), key="nav_reports"):
        st.switch_page("pages/reports.py")
with nav_cols[6]:
    if st.button(translate("instructions", st.session_state.language), key="nav_instructions"):
        st.switch_page("pages/instructions.py")
with nav_cols[7]:
    lang = "en" if st.session_state.language == "ar" else "ar"
    if st.button("عربي/English", key="lang_switch"):
        st.session_state.language = lang
        st.rerun()

# التحقق من تسجيل الدخول
if "user_id" not in st.session_state or not st.session_state.logged_in:
    st.error(translate("login_required", st.session_state.language))
    st.switch_page("app.py")
else:
    fm = FinanceManager(st.session_state.user_id)

    # Welcome Banner
    st.markdown(
        f'<div style="display: flex; justify-content: center; margin: 20px 0;">'
        f'<img src="https://i.ibb.co/KpzDy27r/IMG-2998.png" width="300">'
        f'</div>',
        unsafe_allow_html=True
    )
    
    st.markdown(f"""
        <div style="background-color: #0066cc; color: white; padding: 15px; border-radius: 10px; text-align: center;">
            <h1>{translate("welcome", st.session_state.language)}، {st.session_state.user_id}!</h1>
            <p>{translate("today", st.session_state.language)} {datetime.now().strftime('%A, %d %B %Y')}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Key Metrics Section
    st.subheader(translate("overview", st.session_state.language))
    accounts = fm.get_all_accounts()
    transactions = fm.get_all_transactions()

    if accounts:
        total_balance = sum(acc[3] for acc in accounts)
        income = sum(trans[4] for trans in transactions if trans[3] == "IN")
        expenses = sum(trans[4] for trans in transactions if trans[3] == "OUT")
        net_balance = income - expenses

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                translate("total_balance", st.session_state.language), 
                f"{total_balance:,.2f} {translate('currency', st.session_state.language)}"
            )
        with col2:
            st.metric(
                translate("total_income", st.session_state.language), 
                f"{income:,.2f} {translate('currency', st.session_state.language)}"
            )
        with col3:
            st.metric(
                translate("total_expenses", st.session_state.language), 
                f"{expenses:,.2f} {translate('currency', st.session_state.language)}"
            )
        with col4:
            st.metric(
                translate("net_balance", st.session_state.language), 
                f"{net_balance:,.2f} {translate('currency', st.session_state.language)}",
                delta=f"{net_balance - total_balance:,.2f}" if net_balance != total_balance else None
            )
    else:
        st.info(translate("no_accounts", st.session_state.language))

    st.markdown("---")

    # Alerts Section
    st.subheader(translate("alerts", st.session_state.language))
    alerts = fm.check_alerts()
    if alerts:
        st.warning(alerts)
    else:
        st.success(translate("no_alerts", st.session_state.language))

    st.markdown("---")

    # Visualizations Section
    st.subheader(translate("analysis", st.session_state.language))
    if transactions:
        df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"])
        df["date"] = pd.to_datetime(df["date"])
        df["type"] = df["type"].replace({"IN": translate("total_income", st.session_state.language), 
                                         "OUT": translate("total_expenses", st.session_state.language)})

        # Visualization Type Selector
        viz_type = st.selectbox(
            translate("analysis", st.session_state.language),
            [
                translate("total_income", st.session_state.language) + " vs " + translate("total_expenses", st.session_state.language),
                translate("top_categories", st.session_state.language),
                "Monthly Summary"
            ],
            key="viz_type"
        )

        if viz_type == translate("total_income", st.session_state.language) + " vs " + translate("total_expenses", st.session_state.language):
            # Line Chart for Income and Expenses
            fig = px.line(df, x="date", y="amount", color="type", 
                         title=translate("total_income", st.session_state.language) + " vs " + translate("total_expenses", st.session_state.language), 
                         labels={"amount": translate("currency", st.session_state.language), "date": translate("today", st.session_state.language)})
            st.plotly_chart(fig, use_container_width=True)
        
        elif viz_type == translate("top_categories", st.session_state.language):
            # Pie Chart for Categories
            category_summary = df.groupby("category")["amount"].sum().reset_index()
            fig_pie = px.pie(category_summary, values="amount", names="category", 
                            title=translate("top_categories", st.session_state.language),
                            color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        else:  # Monthly Summary
            df["month"] = df["date"].dt.strftime("%Y-%m")
            monthly_summary = df.groupby(["month", "type"])["amount"].sum().reset_index()
            fig_bar = px.bar(monthly_summary, x="month", y="amount", color="type",
                            title="Monthly Summary",
                            barmode="group",
                            labels={"amount": translate("currency", st.session_state.language), "month": "Month"})
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info(translate("insufficient_data", st.session_state.language))

    st.markdown("---")

    # Recent Transactions Section
    st.subheader(translate("recent_activity", st.session_state.language))
    if transactions:
        recent_transactions = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"]).tail(5)
        recent_transactions["date"] = pd.to_datetime(recent_transactions["date"])
        recent_transactions["type"] = recent_transactions["type"].replace({
            "IN": translate("total_income", st.session_state.language),
            "OUT": translate("total_expenses", st.session_state.language)
        })
        
        # Format the table with styled DataFrame
        st.dataframe(
            recent_transactions[["date", "type", "amount", "description", "category"]].rename(columns={
                "date": translate("today", st.session_state.language),
                "type": "Type",
                "amount": translate("currency", st.session_state.language),
                "description": "Description",
                "category": "Category"
            }),
            column_config={
                translate("currency", st.session_state.language): st.column_config.NumberColumn(
                    format="%.2f " + translate("currency", st.session_state.language)
                )
            },
            use_container_width=True
        )
    else:
        st.info(translate("no_transactions", st.session_state.language))

    st.markdown("---")

    # Top Categories Section
    st.subheader(translate("top_categories", st.session_state.language))
    if transactions:
        with st.expander(translate("view_categories", st.session_state.language)):
            top_categories = df.groupby("category")["amount"].sum().nlargest(5).reset_index()
            st.dataframe(
                top_categories.rename(columns={"category": "Category", "amount": "Amount"}),
                column_config={
                    "Amount": st.column_config.NumberColumn(
                        format="%.2f " + translate("currency", st.session_state.language)
                    )
                },
                use_container_width=True
            )
    else:
        st.info(translate("insufficient_data", st.session_state.language))
