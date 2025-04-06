import streamlit as st
import pandas as pd
from finance_manager import FinanceManager
from datetime import timedelta, datetime
import plotly.express as px
from styles import apply_sidebar_styles
import logging
import time

# تعيين إعدادات الصفحة أولاً
st.set_page_config(
    page_title="FloosAfandy - إحسبها يا عشوائي !!", 
    layout="wide", 
    initial_sidebar_state="auto",
    page_icon="💰"
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

apply_sidebar_styles()

# التحقق من الانتقال إلى صفحة جديدة
if st.session_state.target_page:
    target = st.session_state.target_page
    st.session_state.target_page = None
    st.session_state.collapse_sidebar = True
    st.switch_page(target)

# دالة للترجمة
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
        "account_count": {"ar": "عدد الحسابات", "en": "Account Count"}
    }
    
    if text in translations:
        return translations[text][lang]
    return text

# إذا لم يكن المستخدم مسجلاً الدخول، اعرض واجهة تسجيل/تسجيل دخول
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

    st.title(translate("welcome", st.session_state.language))
    st.image("https://i.ibb.co/KpzDy27r/IMG-2998.png", width=300, use_container_width=True)
    tab1, tab2 = st.tabs([
        translate("login", st.session_state.language),
        translate("signup", st.session_state.language)
    ])

    fm = FinanceManager()  # لا حاجة لـ user_id هنا بعد

    with tab1:  # تسجيل الدخول
        st.subheader(translate("login", st.session_state.language))
        login_username = st.text_input(
            translate("username", st.session_state.language), 
            key="login_username", 
            help=translate("username", st.session_state.language)
        )
        login_password = st.text_input(
            translate("password", st.session_state.language), 
            type="password", 
            key="login_password", 
            help=translate("password", st.session_state.language)
        )
        if st.button(translate("login", st.session_state.language)):
            with st.spinner(translate("login", st.session_state.language) + "..."):
                time.sleep(1)  # Simulate processing
                if fm.verify_user(login_username, login_password):
                    st.session_state.user_id = login_username
                    st.session_state.logged_in = True
                    st.success(f"{translate('welcome', st.session_state.language)}, {login_username}!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

        if st.button(translate("forgot_password", st.session_state.language)):
            st.info(translate("contact_support", st.session_state.language))

    with tab2:  # تسجيل مستخدم جديد
        st.subheader(translate("signup", st.session_state.language))
        new_username = st.text_input(
            translate("new_user", st.session_state.language), 
            key="new_username", 
            help=translate("new_user", st.session_state.language)
        )
        new_password = st.text_input(
            translate("password", st.session_state.language), 
            type="password", 
            key="new_password", 
            help=translate("password", st.session_state.language)
        )
        confirm_password = st.text_input(
            translate("confirm_pass", st.session_state.language), 
            type="password", 
            key="confirm_password", 
            help=translate("confirm_pass", st.session_state.language)
        )
        if st.button(translate("register", st.session_state.language)):
            if new_password == confirm_password:
                if fm.add_user(new_username, new_password):
                    st.success(f"تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول بـ {new_username}")
                else:
                    st.error("اسم المستخدم موجود بالفعل!")
            else:
                st.error("كلمات المرور غير متطابقة!")
else:
    # إذا كان المستخدم مسجلاً الدخول، اعرض الواجهة الرئيسية
    fm = FinanceManager(st.session_state.user_id)

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

        st.image("https://i.ibb.co/KpzDy27r/IMG-2998.png", width=300, use_container_width=True)
        st.markdown(f"<h2>💰 FloosAfandy - {st.session_state.user_id}</h2>", unsafe_allow_html=True)
        alerts = fm.check_alerts()
        if alerts:
            st.markdown(f"<p style='text-align: center; color: #f1c40f;'>⚠️ {len(alerts)} {translate('alerts', st.session_state.language)}</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>الصفحات</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button(translate("home", st.session_state.language), key="nav_home"):
                st.session_state.target_page = "app.py"
                st.rerun()
        with col2:
            if st.button(translate("transactions", st.session_state.language), key="nav_transactions"):
                st.session_state.target_page = "pages/transactions.py"
                st.rerun()

        col3, col4 = st.columns(2)
        with col3:
            if st.button(translate("accounts", st.session_state.language), key="nav_accounts"):
                st.session_state.target_page = "pages/accounts.py"
                st.rerun()
        with col4:
            if st.button(translate("reports", st.session_state.language), key="nav_reports"):
                st.session_state.target_page = "pages/reports.py"
                st.rerun()

        if st.button(translate("logout", st.session_state.language), key="logout"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.rerun()

    st.title(f"إحسبها يا عشوائي !! مرحبًا {st.session_state.user_id}")
    st.markdown("---")

    accounts = fm.get_all_accounts()
    if accounts:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(translate("account_count", st.session_state.language), len(accounts))
        with col2:
            total_balance = sum(acc[3] for acc in accounts)
            st.metric(translate("total_balance", st.session_state.language), f"{total_balance:,.2f}")
        with col3:
            alerts_count = len([acc for acc in accounts if acc[3] < acc[4]])
            st.metric(translate("under_limit", st.session_state.language), alerts_count)

        transactions = fm.get_all_transactions()
        if transactions:
            df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"])
            df["account"] = df["account_id"].map({acc[0]: acc[2] for acc in accounts})
            df["date"] = pd.to_datetime(df["date"])
            
            # Add more visualization options
            viz_type = st.selectbox(
                "نوع التصور",
                ["الرسم الخطي", "الشريطي", "الدائري"],
                key="viz_type"
            )
            
            if viz_type == "الرسم الخطي":
                fig = px.line(df, x="date", y="amount", color="type", 
                              title="المعاملات بمرور الوقت", 
                              labels={"amount": "المبلغ", "date": "التاريخ"}, 
                              height=400)
            elif viz_type == "الشريطي":
                fig = px.bar(df, x="date", y="amount", color="type",
                            title="المعاملات بمرور الوقت",
                            labels={"amount": "المبلغ", "date": "التاريخ"},
                            height=400)
            else:  # دائري
                fig = px.pie(df, values="amount", names="type",
                            title="توزيع المعاملات حسب النوع",
                            height=400)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Show recent transactions table
            st.subheader("آخر المعاملات")
            st.dataframe(df.sort_values("date", ascending=False).head(10), use_container_width=True)
        else:
            st.info(translate("no_transactions", st.session_state.language))
    else:
        st.info(translate("no_accounts", st.session_state.language))

    # إضافة زر مختصر لصفحة معاملاتي
    if st.button(translate("go_to_transactions", st.session_state.language)):
        st.session_state.target_page = "pages/transactions.py"
        st.rerun()
