import streamlit as st

def apply_mobile_styles():
    st.markdown("""
        <style>
            /* Menu button styles */
            .stButton button {
                border-radius: 8px !important;
                padding: 8px 16px !important;
                font-size: 16px !important;
            }
            
            /* Sidebar styles */
            .stSidebar {
                background-color: #f8f9fa;
                padding: 20px;
            }
            
            /* Responsive adjustments */
            @media (max-width: 768px) {
                .stSidebar {
                    width: 100% !important;
                    min-width: 100% !important;
                }
                
                .stButton button {
                    font-size: 14px !important;
                    padding: 6px 12px !important;
                }
            }
        </style>
    """, unsafe_allow_html=True)
