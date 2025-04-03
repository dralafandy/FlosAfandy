import streamlit as st
import pandas as pd
from finance_manager import FinanceManager
from datetime import timedelta, datetime
import plotly.express as px
from styles import apply_sidebar_styles

# تعيين إعدادات الصفحة
st.set_page_config(page_title="FloosAfandy - إحسبها يا عشوائي !!", layout="wide")

# تهيئة الحالة
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "target_page" not in st.session_state:
    st.session_state.target_page = None

apply_sidebar_styles()

# التحقق من الانتقال إلى صفحة جديدة
if st.session_state.target_page:
    target = st.session_state.target_page
    st.session_state.target_page = None
    st.switch_page(target)

# التحقق من تسجيل الدخول
if not st.session_state.logged_in:
    st.image("https://i.ibb.co/KpzDy27r/IMG-2998.png", width=300)
    st.title("مرحبًا بك في FloosAfandy")
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "تسجيل مستخدم جديد"])
    fm = FinanceManager()

    with tab1:
        st.subheader("تسجيل الدخول")
        login_username = st.text_input("اسم المستخدم", key="login_username")
        login_password = st.text_input("كلمة المرور", type="password", key="login_password")
        if st.button("تسجيل الدخول"):
            if fm.verify_user(login_username, login_password):
                st.session_state.user_id = login_username
                st.session_state.logged_in = True
                st.success(f"🎉 مرحبًا {login_username}! لقد تم تسجيل دخولك بنجاح.")
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة!")

    with tab2:
        st.subheader("إنشاء حساب جديد")
        new_username = st.text_input("اسم المستخدم الجديد", key="new_username")
        new_password = st.text_input("كلمة المرور", type="password", key="new_password")
        confirm_password = st.text_input("تأكيد كلمة المرور", type="password", key="confirm_password")
        if st.button("تسجيل"):
            if new_password == confirm_password:
                if fm.add_user(new_username, new_password):
                    st.success(f"✅ تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول بـ {new_username}")
                else:
                    st.error("❌ اسم المستخدم موجود بالفعل!")
            else:
                st.error("❌ كلمات المرور غير متطابقة!")
else:
    # تحميل البيانات بعد تسجيل الدخول
    fm = FinanceManager(st.session_state.user_id)

    # استرجاع الحسابات والمعاملات بعد تسجيل الدخول
    accounts = fm.get_all_accounts(st.session_state.user_id)
    transactions = fm.get_all_transactions(st.session_state.user_id)

    # الشريط الجانبي
    with st.sidebar:
        st.image("https://i.ibb.co/KpzDy27r/IMG-2998.png", width=300)
        st.markdown(f"<h2>💰 FloosAfandy - {st.session_state.user_id}</h2>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>📂 الصفحات</div>", unsafe_allow_html=True)

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

        if st.button("🚪 تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.rerun()

    # الصفحة الرئيسية
    st.title(f"إحسبها يا عشوائي !! مرحبًا {st.session_state.user_id}")
    st.markdown("---")

    if accounts:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("عدد الحسابات", len(accounts))
        with col2:
            total_balance = sum(acc[3] for acc in accounts)
            st.metric("إجمالي الرصيد", f"{total_balance:,.2f} جنيه")
        with col3:
            alerts_count = len([acc for acc in accounts if acc[3] < acc[4]])
            st.metric("حسابات تحت الحد", alerts_count)

        if transactions:
            df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description"])
            df["date"] = pd.to_datetime(df["date"])
            df = df.sort_values(by="date", ascending=False)  # ترتيب المعاملات من الأحدث إلى الأقدم

            # تحليل آخر 30 يومًا
            last_30_days = df[df["date"] >= (datetime.today() - timedelta(days=30))]
            income_last_30 = last_30_days[last_30_days["type"] == "دخل"]["amount"].sum()
            expense_last_30 = last_30_days[last_30_days["type"] == "مصروف"]["amount"].sum()

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 الدخل آخر 30 يوم", f"{income_last_30:,.2f} جنيه")
            with col2:
                st.metric("💸 المصروف آخر 30 يوم", f"{expense_last_30:,.2f} جنيه")
            with col3:
                st.metric("⚖️ الفرق", f"{(income_last_30 - expense_last_30):,.2f} جنيه")

            # تنبيه تجاوز الميزانية
            budget_limit = st.number_input("📏 حدد حد الميزانية الشهرية", min_value=0.0, step=100.0, value=5000.0)
            if expense_last_30 > budget_limit:
                st.error(f"⚠️ تحذير! لقد تجاوزت ميزانيتك الشهرية ({expense_last_30:,.2f} جنيه من {budget_limit:,.2f} جنيه)")

            # رسم بياني للمعاملات
            fig = px.line(df, x="date", y="amount", color="type", title="المعاملات بمرور الوقت", 
                          labels={"amount": "المبلغ", "date": "التاريخ"}, height=400)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ لا توجد معاملات بعد.")
    else:
        st.info("ℹ️ لا توجد حسابات بعد. أضف حسابًا من صفحة 'حساباتي'.")
