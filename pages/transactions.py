import streamlit as st
import pandas as pd
import plotly.express as px
from finance_manager import FinanceManager
from datetime import datetime, timedelta
from mobile_styles import apply_mobile_styles

# تعيين إعدادات الصفحة أولاً
st.set_page_config(
    page_title="FloosAfandy - المعاملات", 
    layout="wide", 
    initial_sidebar_state="collapsed",
    page_icon="💳"
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
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "إضافة معاملة"
if "from_add_transaction" not in st.session_state:
    st.session_state.from_add_transaction = False
if "language" not in st.session_state:
    st.session_state.language = "ar"  # Default to Arabic

apply_mobile_styles()

# دالة للترجمة
def translate(text, lang):
    translations = {
        "transactions": {"ar": "💳 المعاملات", "en": "💳 Transactions"},
        "login_required": {"ar": "يرجى تسجيل الدخول أولاً من الصفحة الرئيسية!", "en": "Please login first from the home page!"},
        "page_title": {"ar": "إدارة المعاملات", "en": "Transactions Management"},
        "page_desc": {"ar": "قم بإدارة وتتبع جميع معاملاتك المالية بسهولة من خلال هذه الصفحة.", "en": "Easily manage and track all your financial transactions through this page."},
        "summary": {"ar": "📊 ملخص المعاملات", "en": "📊 Transactions Summary"},
        "total_income": {"ar": "📥 إجمالي الوارد", "en": "📥 Total Income"},
        "total_expenses": {"ar": "📤 إجمالي المصروفات", "en": "📤 Total Expenses"},
        "net_balance": {"ar": "📊 صافي الرصيد", "en": "📊 Net Balance"},
        "no_transactions": {"ar": "ℹ️ لا توجد معاملات مسجلة حتى الآن.", "en": "ℹ️ No transactions recorded yet."},
        "manage_categories": {"ar": "📂 إدارة الفئات", "en": "📂 Manage Categories"},
        "add_transaction": {"ar": "➕ إضافة معاملة", "en": "➕ Add Transaction"},
        "view_transactions": {"ar": "📋 عرض المعاملات", "en": "📋 View Transactions"},
        "select_account": {"ar": "🏦 اختر الحساب", "en": "🏦 Select Account"},
        "transaction_type": {"ar": "📋 نوع المعاملة", "en": "📋 Transaction Type"},
        "new_category": {"ar": "📛 اسم الفئة الجديدة", "en": "📛 New Category Name"},
        "add_category": {"ar": "➕ إضافة فئة", "en": "➕ Add Category"},
        "current_categories": {"ar": "📋 الفئات الحالية:", "en": "📋 Current Categories:"},
        "delete": {"ar": "🗑️ حذف", "en": "🗑️ Delete"},
        "no_categories": {"ar": "ℹ️ لا توجد فئات.", "en": "ℹ️ No categories."},
        "amount": {"ar": "💵 المبلغ", "en": "💵 Amount"},
        "payment_method": {"ar": "💳 طريقة الدفع", "en": "💳 Payment Method"},
        "description": {"ar": "📝 الوصف", "en": "📝 Description"},
        "save_transaction": {"ar": "💾 حفظ المعاملة", "en": "💾 Save Transaction"},
        "clear_fields": {"ar": "🧹 مسح الحقول", "en": "🧹 Clear Fields"},
        "no_accounts": {"ar": "⚠️ لا توجد حسابات مضافة. يرجى إضافة حساب أولاً.", "en": "⚠️ No accounts added. Please add an account first."},
        "search": {"ar": "🔍 البحث", "en": "🔍 Search"},
        "all": {"ar": "الكل", "en": "All"},
        "income": {"ar": "وارد", "en": "Income"},
        "expense": {"ar": "منصرف", "en": "Expense"},
        "category": {"ar": "📂 الفئة", "en": "📂 Category"},
        "home": {"ar": "🏠 الرئيسية", "en": "🏠 Home"},
        "dashboard": {"ar": "📊 لوحة التحكم", "en": "📊 Dashboard"},
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

    # Page Title and Description
    st.title(translate("page_title", st.session_state.language))
    st.markdown(f"<p style='color: #6b7280;'>{translate('page_desc', st.session_state.language)}</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Summary Section
    st.subheader(translate("summary", st.session_state.language))
    transactions = fm.get_all_transactions()
    if transactions:
        df = pd.DataFrame(transactions, columns=["id", "user_id", "date", "type", "amount", "account_id", "description", "payment_method", "category"])
        df["type"] = df["type"].replace({
            "IN": translate("income", st.session_state.language),
            "OUT": translate("expense", st.session_state.language)
        })
        total_income = df[df["type"] == translate("income", st.session_state.language)]["amount"].sum()
        total_expenses = df[df["type"] == translate("expense", st.session_state.language)]["amount"].sum()
        net_balance = total_income - total_expenses

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                translate("total_income", st.session_state.language), 
                f"{total_income:,.2f} {translate('currency', st.session_state.language)}"
            )
        with col2:
            st.metric(
                translate("total_expenses", st.session_state.language), 
                f"{total_expenses:,.2f} {translate('currency', st.session_state.language)}"
            )
        with col3:
            st.metric(
                translate("net_balance", st.session_state.language), 
                f"{net_balance:,.2f} {translate('currency', st.session_state.language)}",
                delta=f"{net_balance:,.2f}" if net_balance != 0 else None
            )
    else:
        st.info(translate("no_transactions", st.session_state.language))

    st.markdown("---")

    # Tabs for Categories, Adding Transactions, and Viewing Transactions
    tab_names = [
        translate("manage_categories", st.session_state.language),
        translate("add_transaction", st.session_state.language),
        translate("view_transactions", st.session_state.language)
    ]
    tab1, tab2, tab3 = st.tabs(tab_names)

    accounts = fm.get_all_accounts()
    account_options = {acc[0]: acc[2] for acc in accounts}

    # Tab 1: Manage Categories
    with tab1:
        st.subheader(translate("manage_categories", st.session_state.language))
        st.markdown(f"<p style='color: #6b7280;'>{translate('page_desc', st.session_state.language)}</p>", unsafe_allow_html=True)
        st.markdown("---")

        cat_account_id = st.selectbox(
            translate("select_account", st.session_state.language), 
            options=list(account_options.keys()), 
            format_func=lambda x: account_options[x], 
            key="cat_account"
        )
        cat_trans_type = st.selectbox(
            translate("transaction_type", st.session_state.language), 
            [translate("income", st.session_state.language), translate("expense", st.session_state.language)], 
            key="cat_type"
        )
        cat_trans_type_db = "IN" if cat_trans_type == translate("income", st.session_state.language) else "OUT"
        new_category_name = st.text_input(
            translate("new_category", st.session_state.language), 
            placeholder=translate("new_category", st.session_state.language), 
            key="new_category_name"
        )

        if st.button(translate("add_category", st.session_state.language), key="add_category_button"):
            if new_category_name.strip():
                with st.spinner(translate("add_category", st.session_state.language) + "..."):
                    try:
                        fm.add_custom_category(cat_account_id, cat_trans_type_db, new_category_name)
                        st.success(f"✅ {translate('add_category', st.session_state.language)}: {new_category_name}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {str(e)}")
            else:
                st.warning(f"⚠️ {translate('new_category', st.session_state.language)}!")

        categories = fm.get_custom_categories(cat_account_id, cat_trans_type_db)
        if categories:
            st.write(f"{translate('current_categories', st.session_state.language)}")
            for cat in categories:
                cat_name = cat[0]
                col1, col2 = st.columns([3, 1])
                col1.write(f"{'📥' if cat_trans_type_db == 'IN' else '📤'} {cat_name}")
                if col2.button(
                    translate("delete", st.session_state.language), 
                    key=f"del_cat_{cat_name}_{cat_account_id}_{cat_trans_type_db}"
                ):
                    with st.spinner(translate("delete", st.session_state.language) + "..."):
                        try:
                            fm.delete_custom_category_by_name(cat_account_id, cat_trans_type_db, cat_name)
                            st.success(f"🗑️ {translate('delete', st.session_state.language)}: {cat_name}")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {str(e)}")
        else:
            st.info(translate("no_categories", st.session_state.language))

    # Tab 2: Add Transactions
    with tab2:
        st.subheader(translate("add_transaction", st.session_state.language))
        st.markdown(f"<p style='color: #6b7280;'>{translate('page_desc', st.session_state.language)}</p>", unsafe_allow_html=True)
        st.markdown("---")

        if accounts:
            st.session_state.account_id = st.selectbox(
                translate("select_account", st.session_state.language), 
                options=list(account_options.keys()), 
                format_func=lambda x: account_options[x], 
                key="add_account"
            )
            st.session_state.trans_type = st.selectbox(
                translate("transaction_type", st.session_state.language), 
                [translate("income", st.session_state.language), translate("expense", st.session_state.language)], 
                key="add_type"
            )
            trans_type_db = "IN" if st.session_state.trans_type == translate("income", st.session_state.language) else "OUT"

            categories = fm.get_custom_categories(st.session_state.account_id, trans_type_db)
            category_options = [cat[0] for cat in categories] if categories else [translate("all", st.session_state.language)]

            selected_category = st.selectbox(
                translate("category", st.session_state.language), 
                options=category_options, 
                key="add_category"
            )
            amount = st.number_input(
                translate("amount", st.session_state.language), 
                min_value=0.01, 
                value=0.01, 
                step=0.01, 
                format="%.2f", 
                key="add_amount"
            )
            payment_method = st.selectbox(
                translate("payment_method", st.session_state.language), 
                ["كاش", "بطاقة ائتمان", "تحويل بنكي"], 
                key="add_payment"
            )
            description = st.text_area(
                translate("description", st.session_state.language), 
                placeholder=translate("description", st.session_state.language), 
                key="add_desc"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button(translate("save_transaction", st.session_state.language)):
                    with st.spinner(translate("save_transaction", st.session_state.language) + "..."):
                        try:
                            fm.add_transaction(
                                st.session_state.account_id, 
                                amount, 
                                trans_type_db, 
                                description, 
                                payment_method, 
                                selected_category
                            )
                            st.success(f"✅ {translate('save_transaction', st.session_state.language)}!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {str(e)}")
            with col2:
                if st.button(translate("clear_fields", st.session_state.language)):
                    st.session_state.pop("add_amount", None)
                    st.session_state.pop("add_desc", None)
                    st.rerun()
        else:
            st.warning(translate("no_accounts", st.session_state.language))

    # Tab 3: View Transactions
    with tab3:
        st.subheader(translate("view_transactions", st.session_state.language))
        st.markdown(f"<p style='color: #6b7280;'>{translate('page_desc', st.session_state.language)}</p>", unsafe_allow_html=True)
        st.markdown("---")

        if transactions:
            df["account"] = df["account_id"].map(account_options)
            col1, col2, col3 = st.columns(3)
            with col1:
                search_query = st.text_input(translate("search", st.session_state.language), "")
            with col2:
                filter_type = st.selectbox(
                    translate("transaction_type", st.session_state.language), 
                    [translate("all", st.session_state.language), translate("income", st.session_state.language), translate("expense", st.session_state.language)], 
                    key="filter_type"
                )
            with col3:
                filter_category = st.selectbox(
                    translate("category", st.session_state.language), 
                    [translate("all", st.session_state.language)] + list(df["category"].unique()), 
                    key="filter_category"
                )

            filtered_df = df
            if search_query:
                filtered_df = filtered_df[filtered_df.apply(lambda row: search_query.lower() in str(row).lower(), axis=1)]
            if filter_type != translate("all", st.session_state.language):
                filtered_df = filtered_df[filtered_df["type"] == filter_type]
            if filter_category != translate("all", st.session_state.language):
                filtered_df = filtered_df[filtered_df["category"] == filter_category]

            # Format the dataframe for display
            display_df = filtered_df[["date", "type", "amount", "account", "category", "description"]].copy()
            display_df["amount"] = display_df["amount"].apply(lambda x: f"{x:,.2f} {translate('currency', st.session_state.language)}")
            
            st.dataframe(
                display_df.rename(columns={
                    "date": "Date",
                    "type": "Type",
                    "amount": "Amount",
                    "account": "Account",
                    "category": "Category",
                    "description": "Description"
                }),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info(translate("no_transactions", st.session_state.language))
