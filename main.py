# main.py
import streamlit as st
from database import Database
import views

def main():
    # Page Title Context
    st.set_page_config(page_title="Seyahatify - Trip Planner", layout="wide")
    
    # Inject Refined Global CSS for Plus Jakarta Sans and iOS Bento Box styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
        
        /* Apply font safely to core text and structural blocks without breaking native icons */
        html, body, [data-testid="stAppViewContainer"], .stApp, p, h1, h2, h3, h4, h5, h6, label {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Direct targeting for standard buttons and inputs to prevent icon corruption */
        .stButton button, .stTextInput input {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
        }
        
        /* Premium Translucent iOS Bento Card Layout */
        .ios-bento {
            background-color: rgba(142, 142, 147, 0.14);
            border-radius: 18px;
            padding: 24px;
            border: 1px solid rgba(142, 142, 147, 0.22);
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.02);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            margin-bottom: 20px;
        }
        
        /* Bento Header Style */
        .bento-tag {
            text-transform: uppercase; 
            font-size: 11px; 
            letter-spacing: 1.5px; 
            color: #8e8e93; 
            font-weight: 600;
            margin: 0 0 14px 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Bootstrap Database System Setup
    Database.init()

    # Ensure basic configuration defaults exist inside persistent state
    if "page" not in st.session_state:
        st.session_state.page = "auth"
    if "logged_in_user_id" not in st.session_state:
        st.session_state.logged_in_user_id = None
    if "checklist" not in st.session_state:
        st.session_state.checklist = []

    # Route navigation view
    if st.session_state.page == "auth":
        views.create_auth_page()
    elif st.session_state.page == "main":
        views.create_main_page()
    elif st.session_state.page == "history":
        views.create_history_page()

if __name__ == "__main__":
    main()
