import streamlit as st

def apply_mobile_styles():
    st.markdown("""
        <style>
            /* Basic mobile adjustments */
            @media (max-width: 768px) {
                /* Hide sidebar completely on mobile */
                section[data-testid="stSidebar"] {
                    display: none !important;
                }
                
                /* Make content full width on mobile */
                .main .block-container {
                    padding: 1rem 1rem 10rem;
                    width: 100% !important;
                }
                
                /* Adjust font sizes for mobile */
                h1 {
                    font-size: 1.5rem !important;
                }
                
                h2 {
                    font-size: 1.3rem !important;
                }
                
                /* Make buttons more touch-friendly */
                .stButton button {
                    min-width: 100px;
                    padding: 0.5rem;
                }
            }
        </style>
    """, unsafe_allow_html=True)
