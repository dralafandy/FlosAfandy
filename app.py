import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from styles import apply_sidebar_styles

# تعيين إعدادات الصفحة أولاً
st.set_page_config(page_title="FloosAfandy - الرئيسية", layout="wide", initial_sidebar_state="auto")

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

# واجهة تسجيل الدخول أو لوحة التحكم
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.image("https://i.ibb.co/hxjbR4Hv/IMG-2998.png", width=300, use_container_width=True)
    st.title("💰 مرحبًا بك في FloosAfandy")

    st.markdown("<p style='color: #6b7280;'>إدارة أموالك بذكاء وسهولة</p>", unsafe_allow_html=True)
    st.markdown("---")

    with st.form(key="login_form"):
        username = st.text_input("👤 اسم المستخدم")
        password = st.text_input("🔒 كلمة المرور", type="password")
        col1, col2 = st.columns(2)
        with col1:
            login_button = st.form_submit_button("تسجيل الدخول")
        with col2:
            signup_button = st.form_submit_button("إنشاء حساب")

    fm = FinanceManager()
    if login_button:
        if fm.verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.user_id = username
            st.success("✅ تم تسجيل الدخول بنجاح!")
            st.rerun()
        else:
            st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة!")
    if signup_button:
        if fm.add_user(username, password):
            st.success("✅ تم إنشاء الحساب! يمكنك تسجيل الدخول الآن.")
        else:
            st.error("❌ اسم المستخدم موجود بالفعل!")
else:
    fm = FinanceManager(st.session_state.user_id)

    # الشريط الجانبي مع أيقونات
    with st.sidebar:
        st.image("https://i.ibb.co/hxjbR4Hv/IMG-2998.png", width=300, use_container_width=True)
        st.markdown(f"<h2>💰 FloosAfandy - {st.session_state.user_id}</h2>", unsafe_allow_html=True)
        alerts = fm.check_alerts()
        if alerts:
            st.markdown(f"<p style='text-align: center; color: #f1c40f;'>⚠️ {len(alerts)} تنبيهات</p>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>التنقل</div>", unsafe_allow_html=True)
        
        # أزرار التنقل مع أيقونات
        if st.button("📈 لوحة التحكم", key="nav_home", help="عرض الإحصائيات والرسوم البيانية"):
            st.session_state.target_page = "app.py"
            st.rerun()
        if st.button("💸 معاملاتي", key="nav_transactions", help="إضافة وتعديل المعاملات"):
            st.session_state.target_page = "pages/transactions.py"
            st.rerun()
        if st.button("🏦 حساباتي", key="nav_accounts", help="إدارة الحسابات المالية"):
            st.session_state.target_page = "pages/accounts.py"
            st.rerun()
        if st.button("📊 تقاريري", key="nav_reports", help="عرض التقارير المالية"):
            st.session_state.target_page = "pages/reports.py"
            st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("🚪 تسجيل الخروج", key="logout", help="الخروج من الحساب"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.rerun()

    # لوحة التحكم الرئيسية مع Hint
    st.title("📈 لوحة التحكم")
    st.markdown("<p style='color: #6b7280;'>مرحبًا! FloosAfandy يساعدك على تتبع أموالك، إدارة معاملاتك، وتحليل إنفاقك بسهولة.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # جلب البيانات
    accounts = fm.get_all_accounts()
    transactions = fm.get_all_transactions()

    # 1. إجمالي الرصيد
    total_balance = sum(acc[3] for acc in accounts) if accounts else 0.0
    st.metric("💰 إجمالي الرصيد", f"{total_balance:,.2f} جنيه")

    # 2. إحصائيات المعاملات
    if transactions:
        df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"])
        total_in = df[df["type"] == "IN"]["amount"].sum()
        total_out = df[df["type"] == "OUT"]["amount"].sum()
        num_transactions = len(df)
        max_transaction = df["amount"].max()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📥 إجمالي الوارد", f"{total_in:,.2f} جنيه")
        with col2:
            st.metric("📤 إجمالي المنصرف", f"{total_out:,.2f} جنيه")
        with col3:
            st.metric("📋 عدد المعاملات", num_transactions)

        # 3. تنبيهات الحسابات
        if alerts:
            st.subheader("⚠️ التنبيهات")
            for alert in alerts:
                st.warning(alert)

        # 4. رسم بياني لتوزيع الفئات
        st.subheader("📊 توزيع الفئات")
        category_counts = df.groupby("category")["amount"].sum().reset_index()
        fig = px.pie(category_counts, values="amount", names="category", title="توزيع المعاملات حسب الفئة")
        st.plotly_chart(fig, use_container_width=True)

        # 5. رسم بياني للرصيد بمرور الوقت
        st.subheader("📈 الرصيد بمرور الوقت")
        df["date"] = pd.to_datetime(df["date"])
        df_sorted = df.sort_values("date")
        df_sorted["cumulative_balance"] = df_sorted.apply(
            lambda row: row["amount"] if row["type"] == "IN" else -row["amount"], axis=1
        ).cumsum() + total_balance - total_in + total_out
        fig_line = px.line(df_sorted, x="date", y="cumulative_balance", title="تغير الرصيد بمرور الوقت")
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("ℹ️ لا توجد معاملات بعد. ابدأ بإضافة حسابات ومعاملات!")
