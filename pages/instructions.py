import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from mobile_styles import apply_mobile_styles

# تعيين إعدادات الصفحة أولاً
st.set_page_config(page_title="FloosAfandy - التعليمات", layout="wide", initial_sidebar_state="collapsed")

# تهيئة الحالة
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "collapse_sidebar" not in st.session_state:
    st.session_state.collapse_sidebar = False
if "target_page" not in st.session_state:
    st.session_state.target_page = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

apply_mobile_styles()

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



# Page Title
st.title("📖 تعليمات الاستخدام")
st.markdown("<p style='color: #6b7280;'>تعرف على كيفية استخدام برنامج FloosAfandy لإدارة أموالك بسهولة.</p>", unsafe_allow_html=True)
st.markdown("---")

# Instructions Content
st.header("1️⃣ تسجيل الدخول أو إنشاء حساب جديد")
st.markdown("""
- إذا كنت مستخدمًا جديدًا، يمكنك إنشاء حساب جديد من الصفحة الرئيسية.
- إذا كنت تمتلك حسابًا بالفعل، قم بتسجيل الدخول باستخدام اسم المستخدم وكلمة المرور الخاصة بك.
""")

st.header("2️⃣ إدارة الحسابات")
st.markdown("""
- انتقل إلى صفحة **الحسابات** لإضافة حساب جديد.
- أدخل اسم الحساب، الرصيد الافتتاحي، والحد الأدنى للحساب.
- يمكنك تعديل أو حذف الحسابات الموجودة.
""")

st.header("3️⃣ إدارة المعاملات")
st.markdown("""
- انتقل إلى صفحة **المعاملات** لإضافة معاملة جديدة.
- اختر الحساب، نوع المعاملة (وارد أو منصرف)، وأدخل التفاصيل مثل المبلغ والوصف.
- يمكنك تصفية وعرض جميع المعاملات المسجلة.
""")

st.header("4️⃣ عرض التقارير")
st.markdown("""
- انتقل إلى صفحة **التقارير** للحصول على رؤية شاملة لأدائك المالي.
- استخدم الفلاتر لتحديد الحساب، النوع، الفئة، أو الفترة الزمنية.
- قم بتنزيل التقارير كملف CSV.
""")

st.header("5️⃣ لوحة التحكم")
st.markdown("""
- انتقل إلى صفحة **لوحة التحكم** للحصول على ملخص سريع لأموالك.
- شاهد الرسوم البيانية التي تعرض الوارد والمصروفات بمرور الوقت.
- تعرف على أعلى الفئات التي تنفق فيها أموالك.
""")

st.header("6️⃣ إدارة الميزانيات")
st.markdown("""
- انتقل إلى صفحة **إدارة الميزانيات** لإضافة ميزانية جديدة.
- اختر الحساب، أدخل الفئة، وحدد المبلغ المخصص.
- راقب الميزانيات الحالية وتأكد من عدم تجاوزها.
""")

st.header("7️⃣ التنبيهات")
st.markdown("""
- إذا كان أي حساب تحت الحد الأدنى، ستظهر رسالة تنبيه في لوحة التحكم.
- تأكد من متابعة التنبيهات لتجنب أي مشاكل مالية.
""")

st.header("8️⃣ الدعم الفني")
st.markdown("""
- إذا واجهت أي مشاكل، يمكنك التواصل مع الدعم الفني للحصول على المساعدة.
- تأكد من تقديم تفاصيل واضحة حول المشكلة التي تواجهها.
""")

st.markdown("---")
st.info("💡 نصيحة: قم بتجربة جميع الميزات لتتعرف على كيفية إدارة أموالك بشكل أفضل باستخدام FloosAfandy!")
