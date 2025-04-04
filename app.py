import streamlit as st
import pandas as pd
from finance_manager import FinanceManager
from datetime import timedelta, datetime
import plotly.express as px
from components.navigation import show_navigation, show_menu_button

# تعيين إعدادات الصفحة أولاً
st.set_page_config(page_title="FloosAfandy - إحسبها يا عشوائي !!", layout="wide")

# تهيئة الحالة
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True

# Show navigation components
show_navigation()
show_menu_button()

# Handle page navigation
if "collapse_sidebar" not in st.session_state:
    st.session_state.collapse_sidebar = False
# التحقق من الصفحة الحالية
if st.session_state.current_page == "home":
    # Redirect to dashboard if logged in
    if st.session_state.logged_in:
        st.switch_page("pages/dashboard.py")
    else:
        # عرض الصفحة الرئيسية للتسجيل
        st.title("مرحبًا بك في FloosAfandy")
        st.image("https://i.ibb.co/KpzDy27r/IMG-2998.png", width=300, use_container_width=True)
        tab1, tab2 = st.tabs(["🔑 تسجيل الدخول", "🆕 إنشاء حساب جديد"])

        fm = FinanceManager()

        with tab1:  # تسجيل الدخول
            st.subheader("تسجيل الدخول إلى حسابك")
            login_username = st.text_input("اسم المستخدم", key="login_username")
            login_password = st.text_input("كلمة المرور", type="password", key="login_password")
            if st.button("تسجيل الدخول"):
                if fm.verify_user(login_username, login_password):
                    st.session_state.user_id = login_username
                    st.session_state.logged_in = True
                    st.success(f"مرحبًا بك، {login_username}!")
                    st.session_state.current_page = "home"
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

        with tab2:  # تسجيل مستخدم جديد
            st.subheader("إنشاء حساب جديد")
            new_username = st.text_input("اسم المستخدم", key="new_username")
            new_password = st.text_input("كلمة المرور", type="password", key="new_password")
            confirm_password = st.text_input("تأكيد كلمة المرور", type="password", key="confirm_password")
            if st.button("إنشاء الحساب"):
                if new_password == confirm_password:
                    if fm.add_user(new_username, new_password):
                        st.success(f"تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول باستخدام {new_username}.")
                    else:
                        st.error("اسم المستخدم موجود بالفعل!")
                else:
                    st.error("كلمات المرور غير متطابقة!")

elif st.session_state.current_page == "transactions":
    st.switch_page("pages/transactions.py")

elif st.session_state.current_page == "accounts":
    st.switch_page("pages/accounts.py")

elif st.session_state.current_page == "reports":
    st.switch_page("pages/reports.py")

elif st.session_state.current_page == "instructions":
    st.switch_page("pages/instructions.py")
