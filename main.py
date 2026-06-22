# main.py
import streamlit as st
from database import Database
import views

# Ensure basic configuration defaults exist inside persistent state
if "page" not in st.session_state:
    st.session_state.page = "auth"
if "logged_in_user_id" not in st.session_state:
    st.session_state.logged_in_user_id = None
if "checklist" not in st.session_state:
    st.session_state.checklist = []

def main():
    # Page Title Context
    st.set_page_config(page_title="Seyahatify - Trip Planner", layout="wide")
    
    # Bootstrap Database System Setup
    Database.init()

    # Route navigation view
    if st.session_state.page == "auth":
        views.create_auth_page()
    elif st.session_state.page == "main":
        views.create_main_page()
    elif st.session_state.page == "history":
        views.create_history_page()

if __name__ == "__main__":
    main()