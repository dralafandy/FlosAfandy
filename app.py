import streamlit as st
import pandas as pd
from finance_manager import FinanceManager
from datetime import timedelta, datetime
import plotly.express as px
from styles import apply_sidebar_styles
import logging

# تعيين إعدادات الصفحة أولاً
st.set_page_config(page_title="FloosAfandy - إحسبها يا عشوائي !!", layout="wide", initial_sidebar_state="auto")

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

# إذا لم يكن المستخدم مسجلاً الدخول، اعرض واجهة تسجيل/تسجيل دخول
if not st.session_state.logged_in:
    st.title("مرحبًا بك في FloosAfandy")
    st.image("https://i.ibb.co/KpzDy27r/IMG-2998.png", width=300, use_container_width=True)
    tab1, tab2 = st.tabs(["تسجيل الدخول", "تسجيل مستخدم جديد"])

    fm = FinanceManager()  # لا حاجة لـ user_id هنا بعد

    with tab1:  # تسجيل الدخول
        st.subheader("تسجيل الدخول")
        login_username = st.text_input("اسم المستخدم", key="login_username", help="أدخل اسم المستخدم الخاص بك")
        login_password = st.text_input("كلمة المرور", type="password", key="login_password", help="أدخل كلمة المرور الخاصة بك")
        if st.button("تسجيل الدخول"):
            if fm.verify_user(login_username, login_password):
                st.session_state.user_id = login_username
                st.session_state.logged_in = True
                st.success(f"مرحبًا، {login_username}!")
                st.rerun()
            else:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

        if st.button("نسيت كلمة المرور؟"):
            st.info("يرجى الاتصال بالدعم لاستعادة كلمة المرور.")

    with tab2:  # تسجيل مستخدم جديد
        st.subheader("إنشاء حساب جديد")
        new_username = st.text_input("اسم المستخدم الجديد", key="new_username", help="أدخل اسم المستخدم الجديد")
        new_password = st.text_input("كلمة المرور", type="password", key="new_password", help="أدخل كلمة المرور الجديدة")
        confirm_password = st.text_input("تأكيد كلمة المرور", type="password", key="confirm_password", help="أعد إدخال كلمة المرور الجديدة")
        if st.button("تسجيل"):
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
        st.image("https://i.ibb.co/KpzDy27r/IMG-2998.png", width=300, use_container_width=True)
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

    st.title(f"إحسبها يا عشوائي !! مرحبًا {st.session_state.user_id}")
    st.markdown("---")

    accounts = fm.get_all_accounts()
    if accounts:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("عدد الحسابات", len(accounts))
        with col2:
            total_balance = sum(acc[3] for acc in accounts)
            st.metric("إجمالي الرصيد", f"{total_balance:,.2f}")
        with col3:
            alerts_count = len([acc for acc in accounts if acc[3] < acc[4]])
            st.metric("حسابات تحت الحد", alerts_count)

        transactions = fm.get_all_transactions()
        if transactions:
            df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"])
            df["account"] = df["account_id"].map({acc[0]: acc[2] for acc in accounts})
            df["date"] = pd.to_datetime(df["date"])
            fig = px.line(df, x="date", y="amount", color="type", title="المعاملات بمرور الوقت", 
                          labels={"amount": "المبلغ", "date": "التاريخ"}, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ لا توجد معاملات بعد.")
    else:
        st.info("ℹ️ لا توجد حسابات بعد. أضف حسابًا من صفحة 'حساباتي'.")

    # إضافة زر مختصر لصفحة معاملاتي
    if st.button("انتقل إلى صفحة معاملاتي"):
        st.session_state.target_page = "pages/transactions.py"
        st.rerun()
