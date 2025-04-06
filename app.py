import streamlit as st
import pandas as pd
from finance_manager import FinanceManager
from datetime import timedelta, datetime
import plotly.express as px
from styles import apply_sidebar_styles
import logging
import time

# Page configuration
st.set_page_config(
    page_title="FloosAfandy - إحسبها يا عشوائي !!", 
    layout="wide", 
    initial_sidebar_state="auto",
    page_icon="💰",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "### FloosAfandy - Personal Finance Manager\nVersion 1.0"
    }
)

# Initialize session state
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

apply_sidebar_styles()

# Translation function
def translate(text, lang):
    translations = {
        "welcome": {"ar": "مرحبًا بك في FloosAfandy", "en": "Welcome to FloosAfandy"},
        "login": {"ar": "تسجيل الدخول", "en": "Login"},
        "signup": {"ar": "تسجيل مستخدم جديد", "en": "Sign Up"},
        "username": {"ar": "اسم المستخدم", "en": "Username"},
        "password": {"ar": "كلمة المرور", "en": "Password"},
        "forgot_password": {"ar": "نسيت كلمة المرور؟", "en": "Forgot password?"},
        "new_user": {"ar": "اسم المستخدم الجديد", "en": "New username"},
        "confirm_pass": {"ar": "تأكيد كلمة المرور", "en": "Confirm password"},
        "register": {"ar": "تسجيل", "en": "Register"},
        "contact_support": {"ar": "يرجى الاتصال بالدعم لاستعادة كلمة المرور.", "en": "Please contact support to recover your password."},
        "home": {"ar": "🏠 الرئيسية", "en": "🏠 Home"},
        "transactions": {"ar": "💸 معاملاتي", "en": "💸 Transactions"},
        "accounts": {"ar": "🏦 حساباتي", "en": "🏦 Accounts"},
        "reports": {"ar": "📊 تقاريري", "en": "📊 Reports"},
        "logout": {"ar": "تسجيل الخروج", "en": "Logout"},
        "total_balance": {"ar": "إجمالي الرصيد", "en": "Total Balance"},
        "under_limit": {"ar": "حسابات تحت الحد", "en": "Accounts Under Limit"},
        "no_transactions": {"ar": "ℹ️ لا توجد معاملات بعد.", "en": "ℹ️ No transactions yet."},
        "no_accounts": {"ar": "ℹ️ لا توجد حسابات بعد. أضف حسابًا من صفحة 'حساباتي'.", "en": "ℹ️ No accounts yet. Add an account from 'Accounts' page."},
        "go_to_transactions": {"ar": "انتقل إلى صفحة معاملاتي", "en": "Go to Transactions"},
        "alerts": {"ar": "تنبيهات", "en": "Alerts"},
        "account_count": {"ar": "عدد الحسابات", "en": "Account Count"},
        "app_title": {"ar": "إحسبها يا عشوائي !!", "en": "Calculate It Randomly !!"},
        "welcome_back": {"ar": "مرحبًا بعودتك،", "en": "Welcome back,"},
        "dashboard": {"ar": "لوحة التحكم", "en": "Dashboard"},
        "quick_stats": {"ar": "إحصائيات سريعة", "en": "Quick Stats"},
        "recent_activity": {"ar": "النشاط الأخير", "en": "Recent Activity"},
        "currency": {"ar": "جنيه", "en": "EGP"}
    }
    
    if text in translations:
        return translations[text][lang]
    return text

# Check for page redirection
if st.session_state.target_page:
    target = st.session_state.target_page
    st.session_state.target_page = None
    st.session_state.collapse_sidebar = True
    st.switch_page(target)

# Login/Signup Page
if not st.session_state.logged_in:
    # Language selector
    lang_col1, lang_col2 = st.columns(2)
    with lang_col1:
        if st.button("العربية", key="lang_ar"):
            st.session_state.language = "ar"
            st.rerun()
    with lang_col2:
        if st.button("English", key="lang_en"):
            st.session_state.language = "en"
            st.rerun()

    # Welcome section
    st.markdown(
        f"""
        <div style="text-align: center; margin-bottom: 30px;">
            <img src="https://i.ibb.co/KpzDy27r/IMG-2998.png" width="250">
            <h1 style="color: #2c3e50; margin-top: 10px;">{translate("welcome", st.session_state.language)}</h1>
            <p style="color: #7f8c8d;">{translate("app_title", st.session_state.language)}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Login/Signup tabs
    tab1, tab2 = st.tabs([
        translate("login", st.session_state.language),
        translate("signup", st.session_state.language)
    ])

    fm = FinanceManager()

    with tab1:  # Login
        with st.form("login_form"):
            st.subheader(translate("login", st.session_state.language))
            login_username = st.text_input(
                translate("username", st.session_state.language), 
                key="login_username"
            )
            login_password = st.text_input(
                translate("password", st.session_state.language), 
                type="password", 
                key="login_password"
            )
            
            login_col1, login_col2 = st.columns([3, 1])
            with login_col1:
                login_submitted = st.form_submit_button(translate("login", st.session_state.language))
            with login_col2:
                if st.button(translate("forgot_password", st.session_state.language)):
                    st.info(translate("contact_support", st.session_state.language))

            if login_submitted:
                with st.spinner(translate("login", st.session_state.language) + "..."):
                    time.sleep(1)  # Simulate processing
                    if fm.verify_user(login_username, login_password):
                        st.session_state.user_id = login_username
                        st.session_state.logged_in = True
                        st.success(f"{translate('welcome_back', st.session_state.language)} {login_username}!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

    with tab2:  # Signup
        with st.form("signup_form"):
            st.subheader(translate("signup", st.session_state.language))
            new_username = st.text_input(
                translate("new_user", st.session_state.language), 
                key="new_username"
            )
            new_password = st.text_input(
                translate("password", st.session_state.language), 
                type="password", 
                key="new_password"
            )
            confirm_password = st.text_input(
                translate("confirm_pass", st.session_state.language), 
                type="password", 
                key="confirm_password"
            )
            
            if st.form_submit_button(translate("register", st.session_state.language)):
                if new_password == confirm_password:
                    if new_password.strip() and new_username.strip():
                        if fm.add_user(new_username, new_password):
                            st.success(f"✅ تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول بـ {new_username}")
                        else:
                            st.error("اسم المستخدم موجود بالفعل!")
                    else:
                        st.error("يجب ألا تكون الحقول فارغة!")
                else:
                    st.error("كلمات المرور غير متطابقة!")

# Main App Page
else:
    fm = FinanceManager(st.session_state.user_id)

    # Sidebar
    with st.sidebar:
        # Language selector
        lang_col1, lang_col2 = st.columns(2)
        with lang_col1:
            if st.button("العربية", key="sidebar_lang_ar"):
                st.session_state.language = "ar"
                st.rerun()
        with lang_col2:
            if st.button("English", key="sidebar_lang_en"):
                st.session_state.language = "en"
                st.rerun()

        # User profile section
        st.markdown(
            f"""
            <div style="text-align: center; margin-bottom: 20px;">
                <img src="https://i.ibb.co/KpzDy27r/IMG-2998.png" width="150">
                <h3 style="color: #2c3e50; margin-top: 10px;">💰 FloosAfandy</h3>
                <p style="color: #3498db; font-weight: bold;">{st.session_state.user_id}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Alerts
        alerts = fm.check_alerts()
        if alerts:
            st.markdown(
                f"<div style='background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px;'>"
                f"⚠️ {len(alerts)} {translate('alerts', st.session_state.language)}"
                f"</div>",
                unsafe_allow_html=True
            )
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Navigation
        st.markdown("<div class='section-title'>الصفحات</div>", unsafe_allow_html=True)
        
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button(translate("home", st.session_state.language), key="nav_home"):
                st.session_state.target_page = "app.py"
                st.rerun()
        with nav_col2:
            if st.button(translate("transactions", st.session_state.language), key="nav_transactions"):
                st.session_state.target_page = "pages/transactions.py"
                st.rerun()

        nav_col3, nav_col4 = st.columns(2)
        with nav_col3:
            if st.button(translate("accounts", st.session_state.language), key="nav_accounts"):
                st.session_state.target_page = "pages/accounts.py"
                st.rerun()
        with nav_col4:
            if st.button(translate("reports", st.session_state.language), key="nav_reports"):
                st.session_state.target_page = "pages/reports.py"
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        
        if st.button(translate("logout", st.session_state.language), key="logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.rerun()

    # Main content
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h1 style="color: #2c3e50;">{translate('app_title', st.session_state.language)}</h1>
            <p style="color: #7f8c8d;">{datetime.now().strftime('%A, %d %B %Y')}</p>
        </div>
        <h3 style="color: #3498db; margin-bottom: 30px;">{translate('welcome_back', st.session_state.language)} {st.session_state.user_id}!</h3>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Quick Stats Section
    st.subheader(translate("quick_stats", st.session_state.language))
    accounts = fm.get_all_accounts()
    
    if accounts:
        total_balance = sum(acc[3] for acc in accounts)
        under_limit_count = len([acc for acc in accounts if acc[3] < acc[4]])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                translate("account_count", st.session_state.language), 
                len(accounts),
                help="إجمالي عدد الحسابات المسجلة"
            )
        with col2:
            st.metric(
                translate("total_balance", st.session_state.language), 
                f"{total_balance:,.2f} {translate('currency', st.session_state.language)}",
                help="إجمالي الرصيد عبر جميع الحسابات"
            )
        with col3:
            st.metric(
                translate("under_limit", st.session_state.language), 
                under_limit_count,
                delta=f"-{under_limit_count}" if under_limit_count > 0 else None,
                delta_color="inverse",
                help="عدد الحسابات تحت الحد الأدنى"
            )
    else:
        st.info(translate("no_accounts", st.session_state.language))
    
    st.markdown("---")
    
    # Recent Activity Section
    st.subheader(translate("recent_activity", st.session_state.language))
    transactions = fm.get_all_transactions()
    
    if transactions:
        df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"])
        df["account"] = df["account_id"].map({acc[0]: acc[2] for acc in accounts})
        df["date"] = pd.to_datetime(df["date"])
        
        # Visualization selector
        viz_type = st.selectbox(
            "اختر نوع التصور",
            ["الرسم الخطي", "الشريطي", "الدائري"],
            key="viz_type"
        )
        
        if viz_type == "الرسم الخطي":
            fig = px.line(
                df, 
                x="date", 
                y="amount", 
                color="type", 
                title="المعاملات بمرور الوقت", 
                labels={
                    "amount": f"المبلغ ({translate('currency', st.session_state.language)})", 
                    "date": "التاريخ"
                }, 
                height=400
            )
        elif viz_type == "الشريطي":
            fig = px.bar(
                df, 
                x="date", 
                y="amount", 
                color="type",
                title="المعاملات بمرور الوقت",
                labels={
                    "amount": f"المبلغ ({translate('currency', st.session_state.language)})", 
                    "date": "التاريخ"
                },
                height=400
            )
        else:  # دائري
            fig = px.pie(
                df, 
                values="amount", 
                names="type",
                title="توزيع المعاملات حسب النوع",
                height=400
            )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recent transactions table
        st.markdown("### آخر المعاملات")
        recent_df = df.sort_values("date", ascending=False).head(5)
        st.dataframe(
            recent_df[["date", "type", "amount", "account", "description"]],
            column_config={
                "date": "التاريخ",
                "type": "النوع",
                "amount": st.column_config.NumberColumn(
                    "المبلغ",
                    format=f"%.2f {translate('currency', st.session_state.language)}"
                ),
                "account": "الحساب",
                "description": "الوصف"
            },
            use_container_width=True,
            hide_index=True
        )
        
        # Quick action button
        st.markdown("---")
        if st.button(translate("go_to_transactions", st.session_state.language), type="primary"):
            st.session_state.target_page = "pages/transactions.py"
            st.rerun()
    else:
        st.info(translate("no_transactions", st.session_state.language))
