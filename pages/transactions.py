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
st.set_page_config(page_title="FloosAfandy - معاملاتي", layout="wide", initial_sidebar_state=sidebar_state)

apply_sidebar_styles()

# التحقق من الانتقال إلى صفحة جديدة
if st.session_state.target_page:
    target = st.session_state.target_page
    st.session_state.target_page = None
    st.session_state.collapse_sidebar = True
    st.switch_page(target)

# التخزين المؤقت للبيانات
@st.cache_data
def get_all_transactions():
    fm = FinanceManager()
    return fm.get_all_transactions()

@st.cache_data
def get_all_accounts():
    fm = FinanceManager()
    return fm.get_all_accounts()

@st.cache_data
def get_custom_categories(account_id, trans_type):
    fm = FinanceManager()
    return fm.get_custom_categories(account_id, trans_type)

with st.sidebar:
    st.image("https://i.ibb.co/hxjbR4Hv/IMG-2998.png", width=300, use_container_width=True)
    st.markdown("<h2>💰 FloosAfandy</h2>", unsafe_allow_html=True)
    fm = FinanceManager()
    alerts = fm.check_alerts()
    if alerts:
        st.markdown(f"<p style='text-align: center; color: #f1c40f;'>⚠️ {len(alerts)} تنبيهات</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown("<div class='section-title'>الصفحات</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        btn_style = "background: linear-gradient(90deg, #B8E8EF, #A0E0DB);" if "app.py" == "app.py" else ""
        st.markdown(f"<style>#nav_home {{ {btn_style} }}</style>", unsafe_allow_html=True)
        if st.button("📈 لوحة التحكم", key="nav_home"):
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

# Main content
st.title("💸 معاملاتي")
st.markdown("<p style='color: #6b7280;'>سجل وتحكم في كل حركة مالية</p>", unsafe_allow_html=True)
st.markdown("---")

# CSS للتحسينات البصرية
st.markdown("""
    <style>
    .transaction-card {background-color: #ffffff; padding: 10px; border-radius: 8px; margin: 5px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: transform 0.2s;}
    .transaction-card:hover {transform: translateY(-2px);}
    .form-container {background-color: #f9fafb; padding: 15px; border-radius: 10px; margin-bottom: 15px;}
    .category-container {background-color: #e5e7eb; padding: 15px; border-radius: 10px; margin-bottom: 20px;}
    </style>
""", unsafe_allow_html=True)

# علامات تبويب
tab1, tab2, tab3 = st.tabs(["📂 إدارة الفئات", "➕ إضافة معاملة", "📋 المعاملات"])

accounts = get_all_accounts()
account_options = {acc[0]: acc[1] for acc in accounts}

# Tab 1: إدارة الفئات
with tab1:
    with st.container():
        st.markdown("<div class='category-container'>", unsafe_allow_html=True)
        cat_account_id = st.selectbox("🏦 الحساب", options=list(account_options.keys()), 
                                      format_func=lambda x: account_options[x], key="cat_account")
        cat_trans_type = st.selectbox("📋 النوع", ["وارد", "منصرف"], key="cat_type")
        cat_trans_type_db = "IN" if cat_trans_type == "وارد" else "OUT"
        new_category_name = st.text_input("📛 اسم الفئة الجديدة", placeholder="مثال: مكافأة", key="new_category_name")
        
        if st.button("➕ إضافة فئة", key="add_category_button"):
            if new_category_name.strip():
                with st.spinner("جارٍ الإضافة..."):
                    try:
                        fm.add_custom_category(cat_account_id, cat_trans_type_db, new_category_name)
                        st.success(f"✅ تمت إضافة الفئة: {new_category_name}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
            else:
                st.warning("⚠️ أدخل اسمًا للفئة!")
        
        categories = get_custom_categories(cat_account_id, cat_trans_type_db)
        if categories:
            st.write("الفئات الحالية:")
            for cat in categories:
                cat_name = cat[0]
                col1, col2 = st.columns([3, 1])
                col1.write(f"{'📥' if cat_trans_type_db == 'IN' else '📤'} {cat_name}")
                if col2.button("🗑️", key=f"del_cat_{cat_name}_{cat_account_id}_{cat_trans_type_db}"):
                    if st.checkbox(f"تأكيد حذف {cat_name}", key=f"confirm_del_{cat_name}"):
                        try:
                            fm.delete_custom_category_by_name(cat_account_id, cat_trans_type_db, cat_name)
                            st.success(f"🗑️ تم حذف الفئة: {cat_name}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ خطأ: {str(e)}")
        else:
            st.info("ℹ️ لا توجد فئات.")
        st.markdown("</div>", unsafe_allow_html=True)

# Tab 2: إضافة معاملة
with tab2:
    if "trans_type" not in st.session_state:
        st.session_state.trans_type = "وارد"
    if "account_id" not in st.session_state:
        st.session_state.account_id = list(account_options.keys())[0] if accounts else None

    # تحديث القيم عند تغيير الحساب أو نوع المعاملة
    st.session_state.account_id = st.selectbox(
        "🏦 الحساب", 
        options=list(account_options.keys()), 
        format_func=lambda x: account_options[x], 
        key="add_account",
        index=list(account_options.keys()).index(st.session_state.account_id)
    )
    st.session_state.trans_type = st.selectbox(
        "📋 نوع المعاملة", 
        ["وارد", "منصرف"], 
        key="add_type",
        index=0 if st.session_state.trans_type == "وارد" else 1
    )
    trans_type_db = "IN" if st.session_state.trans_type == "وارد" else "OUT"

    # Fetch the latest categories data
    categories = get_custom_categories(st.session_state.account_id, trans_type_db)
    category_options = [cat[0] for cat in categories] if categories else ["غير مصنف"]

    # عناصر الإدخال
    selected_category = st.selectbox(
        "📂 الفئة", 
        options=category_options, 
        key="add_category"
    )
    amount = st.number_input("💵 المبلغ", min_value=0.01, step=0.01, format="%.2f", key="add_amount")
    payment_method = st.selectbox("💳 طريقة الدفع", ["كاش", "بطاقة ائتمان", "تحويل بنكي"], key="add_payment")
    description = st.text_area("📝 الوصف", placeholder="وصف المعاملة (اختياري)", key="add_desc")

    # أزرار الإجراءات
    col5, col6, col7 = st.columns(3)
    with col5:
        submit_button = st.button("💾 حفظ", key="submit_transaction")
    with col6:
        submit_add_another = st.button("➕ حفظ وإضافة", key="submit_add_another")
    with col7:
        reset_button = st.button("🧹 مسح", key="reset_transaction")

    # معالجة الإجراءات
    if submit_button or submit_add_another:
        # Fetch the latest accounts and categories again before saving
        accounts = get_all_accounts()
        account_options = {acc[0]: acc[1] for acc in accounts}
        categories = get_custom_categories(st.session_state.account_id, trans_type_db)
        category_options = [cat[0] for cat in categories] if categories else ["غير مصنف"]

        with st.spinner("جارٍ الحفظ..."):
            try:
                final_trans_type_db = "IN" if st.session_state.trans_type == "وارد" else "OUT"
                final_category = selected_category if selected_category in category_options else "غير مصنف"
                result = fm.add_transaction(st.session_state.account_id, amount, final_trans_type_db, description, payment_method, final_category)
                st.success(f"✅ تم حفظ المعاملة بالفئة: {final_category}")
                if result and "تنبيه" in result:
                    st.warning(result)
                if submit_add_another:
                    st.session_state["trans_type"] = st.session_state.trans_type
                    st.session_state["account_id"] = st.session_state.account_id
                else:
                    st.rerun()
            except Exception as e:
                st.error(f"❌ خطأ: {str(e)}")
    if reset_button:
        st.session_state.pop("add_amount", None)
        st.session_state.pop("add_desc", None)
        st.rerun()

# Tab 3: المعاملات
with tab3:
    transactions = get_all_transactions()
    if transactions:
        df = pd.DataFrame(transactions, columns=["id", "date", "type", "amount", "account_id", "description", "payment_method", "category"])
        df["account"] = df["account_id"].map(account_options)
        df["type"] = df["type"].replace({"IN": "وارد", "OUT": "منصرف"})

        # فلاتر متقدمة
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            search_query = st.text_input("🔍 البحث", "")
        with col_f2:
            filter_type = st.selectbox("📋 النوع", ["الكل", "وارد", "منصرف"], key="filter_type")
        with col_f3:
            filter_category = st.selectbox("📂 الفئة", ["الكل"] + list(df["category"].unique()), key="filter_category")

        filtered_df = df
        if search_query:
            filtered_df = filtered_df[filtered_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]
        if filter_type != "الكل":
            filtered_df = filtered_df[filtered_df["type"] == filter_type]
        if filter_category != "الكل":
            filtered_df = filtered_df[filtered_df["category"] == filter_category]

        # عرض الجدول التفاعلي
        st.dataframe(filtered_df[["date", "type", "amount", "account", "category", "description"]], use_container_width=True)

        # تعديل أو حذف
        st.subheader("🛠️ تعديل أو حذف")
        trans_id = st.selectbox("اختر معاملة", options=filtered_df["id"].tolist(), 
                                format_func=lambda x: f"معاملة {x} - {filtered_df[filtered_df['id'] == x]['date'].iloc[0]} - {filtered_df[filtered_df['id'] == x]['category'].iloc[0]}")
        selected_trans = filtered_df[filtered_df["id"] == trans_id].iloc[0]
        with st.form(key="edit_transaction_form"):
            st.markdown("<div class='form-container'>", unsafe_allow_html=True)
            edit_account = st.selectbox("🏦 الحساب", options=list(account_options.keys()), 
                                        index=list(account_options.keys()).index(selected_trans["account_id"]), key="edit_account")
            edit_type = st.selectbox("📋 النوع", ["وارد", "منصرف"], 
                                     index=0 if selected_trans["type"] == "وارد" else 1, key="edit_type")
            edit_type_db = "IN" if edit_type == "وارد" else "OUT"
            edit_categories = get_custom_categories(edit_account, edit_type_db)
            edit_category_options = [cat[0] for cat in edit_categories] if edit_categories else ["غير مصنف"]
            edit_selected_category = st.selectbox("📂 الفئة", options=edit_category_options, 
                                                  index=edit_category_options.index(selected_trans["category"]) if selected_trans["category"] in edit_category_options else 0, 
                                                  key="edit_category")
            edit_amount = st.number_input("💵 المبلغ", value=float(selected_trans["amount"]), min_value=0.01, step=0.01, format="%.2f", key="edit_amount")
            edit_payment = st.selectbox("💳 طريقة الدفع", ["كاش", "بطاقة ائتمان", "تحويل بنكي"], 
                                        index=["كاش", "بطاقة ائتمان", "تحويل بنكي"].index(selected_trans["payment_method"]), key="edit_payment")
            edit_desc = st.text_area("📝 الوصف", value=selected_trans["description"], key="edit_desc")
            st.markdown("</div>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                save_button = st.form_submit_button("💾 حفظ التعديل")
            with col2:
                delete_button = st.form_submit_button("🗑️ حذف")

        if save_button:
            with st.spinner("جارٍ التعديل..."):
                try:
                    final_edit_category = edit_selected_category if edit_selected_category in edit_category_options else "غير مصنف"
                    result = fm.edit_transaction(trans_id, edit_account, edit_amount, edit_type_db, edit_desc, edit_payment, final_edit_category)
                    st.success(f"✅ تم التعديل: {final_edit_category}")
                    if result and "تنبيه" in result:
                        st.warning(result)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ: {str(e)}")

        if delete_button:
            if st.checkbox(f"تأكيد حذف المعاملة {trans_id}", key=f"confirm_del_trans_{trans_id}"):
                with st.spinner("جارٍ الحذف..."):
                    try:
                        with fm.conn:
                            old_trans = fm.conn.execute('SELECT type, amount, account_id FROM transactions WHERE id = ?', (trans_id,)).fetchone()
                            old_type, old_amount, old_account_id = old_trans
                            fm.conn.execute('UPDATE accounts SET balance = balance + ? WHERE id = ?', 
                                            (old_amount if old_type == "IN" else -old_amount, old_account_id))
                            fm.conn.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
                            fm.conn.commit()
                        st.success("🗑️ تم الحذف!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {str(e)}")
    else:
        st.info("ℹ️ لا توجد معاملات.")
