import streamlit as st

def apply_sidebar_styles():
    st.markdown("""
        <style>
        .stApp {
            background-color: #f9f9f9;
            font-family: Arial, sans-serif;
            font-size: 15px;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            color: #444444;
            padding: 20px;
            max-width: 300px;
            border-left: 1px solid #dddddd;
        }
        .sidebar h2 {
            color: #444444;
            font-size: 18px;
            text-align: left;
            margin: 15px 0;
            font-weight: bold;
        }
        .sidebar hr {
            border: none;
            border-top: 1px solid #eeeeee;
            margin: 15px 0;
        }
        .stButton>button {
            background-color: #0066cc;
            color: #ffffff;
            border-radius: 4px;
            padding: 10px;
            font-size: 13px;
            font-weight: bold;
            width: 100%;
            border: none;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #005bb5;
        }
        .stSelectbox, .stTextInput {
            background-color: #ffffff;
            color: #444444;
            border-radius: 4px;
            padding: 8px;
            font-size: 13px;
            border: 1px solid #cccccc;
            margin-bottom: 10px;
        }
        [data-testid="stSidebarNav"] {
            display: none !important;
        }
        .section-title {
            color: #444444;
            font-size: 12px;
            margin: 10px 0 5px 0;
            text-transform: uppercase;
            font-weight: bold;
        }
        @media (max-width: 768px) {
            .stApp {
                font-size: 14px;
            }
            .sidebar .sidebar-content {
                max-width: 100%;
                border-left: none;
            }
            .stButton>button {
                font-size: 12px;
                padding: 8px;
            }
        }
        </style>
    """, unsafe_allow_html=True)