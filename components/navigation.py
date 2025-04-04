import streamlit as st
from mobile_styles import apply_mobile_styles

def show_navigation():
    """Centralized navigation component for the app"""
    apply_mobile_styles()
    
    # Sidebar navigation
    with st.sidebar:
        st.header("🔗 القائمة الرئيسية")
        
        if st.button("🏠 الصفحة الرئيسية"):
            st.session_state.current_page = "home"
            st.rerun()
            
        if st.button("📊 لوحة التحكم"):
            st.session_state.current_page = "dashboard"
            st.rerun()
            
        if st.button("💳 المعاملات"):
            st.session_state.current_page = "transactions" 
            st.rerun()
            
        if st.button("🏦 الحسابات"):
            st.session_state.current_page = "accounts"
            st.rerun()
            
        if st.button("📈 التقارير"):
            st.session_state.current_page = "reports"
            st.rerun()
            
        if st.button("📚 التعليمات"):
            st.session_state.current_page = "instructions"
            st.rerun()
            
        st.markdown("---")
        
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.logged_in = False
            st.session_state.user_id = None
            st.session_state.current_page = "home"
            st.rerun()

def show_menu_button():
    """Shows the menu toggle button in the main content"""
    if st.button("☰ القائمة"):
        st.session_state.show_sidebar = not st.session_state.get('show_sidebar', True)
        st.rerun()
