# views.py
import streamlit as st
from database import Database

def create_auth_page():
    st.title("Seyahatify")
    tab1, tab2 = st.tabs(["Log In", "Sign Up"])

    with tab1:
        st.subheader("Log In to Your Account")
        login_user = st.text_input("Username", key="login_user")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        
        if st.button("Login", type="primary"):
            user_id = Database.login(login_user, login_pass)
            if user_id:
                st.session_state.logged_in_user_id = user_id
                st.session_state.page = "main"
                st.rerun()
            else:
                st.error("Incorrect username or password!")

    with tab2:
        st.subheader("Create a New Account")
        reg_user = st.text_input("Create a Username", key="reg_user")
        reg_pass = st.text_input("Create a Password", type="password", key="reg_pass")
        
        if st.button("Register"):
            if not reg_user or not reg_pass:
                st.warning("Fields cannot be empty!")
            elif Database.register(reg_user, reg_pass):
                st.success("Account created! You can now log in.")
            else:
                st.error("Username already exists!")

def create_main_page():
    # --- SIDEBAR (Trip Checklist) ---
    with st.sidebar:
        st.header("✓ Trip Checklist")
        
        # Add new Item
        new_todo = st.text_input("Add personal mission item:", key="todo_input")
        if st.button("+ Add Item", use_container_width=True):
            if new_todo.strip():
                st.session_state.checklist.append({"text": new_todo.strip(), "checked": False})
                st.rerun()

        # Render Active Checklist Items
        updated_checklist = []
        for idx, item in enumerate(st.session_state.checklist):
            is_checked = st.checkbox(item["text"], value=item["checked"], key=f"todo_check_{idx}")
            updated_checklist.append({"text": item["text"], "checked": is_checked})
        st.session_state.checklist = updated_checklist

        # Action Buttons
        if st.button("Remove Checked", use_container_width=True):
            st.session_state.checklist = [item for item in st.session_state.checklist if not item["checked"]]
            st.rerun()

        st.markdown("---")
        
        if st.button("💾 Save Trip", type="primary", use_container_width=True):
            city = st.session_state.get("city_search_val", "").strip()
            if not city:
                st.warning("Please enter a destination city before saving the trip!")
            elif not st.session_state.checklist:
                st.warning("Add at least one item to your checklist!")
            else:
                Database.save_trip(st.session_state.logged_in_user_id, city, st.session_state.checklist)
                st.success(f"Trip to {city.title()} saved successfully!")

        if st.button("📋 View History", use_container_width=True):
            st.session_state.page = "history"
            st.rerun()

    # --- MAIN CONTENT AREA ---
    st.header("Where would you like to travel?")
    
    # Target Search
    city_entry = st.text_input("Enter city name:", value=st.session_state.get("city_search_val", ""))
    
    if st.button("🔍 Search", type="primary"):
        if city_entry.strip():
            st.session_state.city_search_val = city_entry.strip()
            st.session_state.weather_cache = Database.fetch_weather(city_entry.strip())
            st.session_state.news_cache = Database.fetch_news(city_entry.strip())
            st.rerun()
        else:
            st.warning("Please enter a valid city name!")

    # Weather Block Display
    st.subheader("🌤 Weather Information")
    if "weather_cache" in st.session_state:
        if "⚠" in st.session_state.weather_cache:
            st.error(st.session_state.weather_cache)
        else:
            st.info(f"**📍 {st.session_state.city_search_val.title()}**\n\n{st.session_state.weather_cache}")
    else:
        st.write("Enter a city and click search to see weather information.")

    # News Block Display
    st.subheader("📰 Latest News")
    if "news_cache" in st.session_state and st.session_state.news_cache:
        for idx, article in enumerate(st.session_state.news_cache, 1):
            with st.container(border=True):
                st.markdown(f"**{idx}. {article.get('title', 'No title')}**")
                st.markdown(f"[🔗 Click to read more]({article.get('url', '')})")
    elif "news_cache" in st.session_state:
        st.write("No recent news found for this city.")
    else:
        st.write("Top headlines will appear here after searching.")

def create_history_page():
    st.header("Your Saved Trips")
    
    if st.button("← Back to Dashboard"):
        st.session_state.page = "main"
        st.rerun()

    sort_option = st.selectbox("Sort Context:", ["🕐 Newest", "🕰 Oldest", "🔤 A → Z"])
    sort_mapping = {"🕐 Newest": "newest", "🕰 Oldest": "oldest", "🔤 A → Z": "atoz"}
    sort_mode = sort_mapping[sort_option]

    sorted_trips = Database.load_trips(st.session_state.logged_in_user_id, sort_mode)

    if not sorted_trips:
        st.info("No saved trips yet. Create a trip from the main dashboard!")
        return

    # Modern Bento Grid Representation using Columns
    cols = st.columns(2)
    for idx, (trip_id, city) in enumerate(sorted_trips):
        with cols[idx % 2]:
            with st.container(border=True):
                head_col1, head_col2 = st.columns([4, 1])
                head_col1.markdown(f"### ✈  {city.title()}")
                
                if head_col2.button("🗑", key=f"del_{trip_id}"):
                    Database.delete_trip(trip_id)
                    st.toast(f"Trip to {city.title()} deleted.")
                    st.rerun()

                st.markdown("**🌤 Weather Context**")
                st.caption(Database.fetch_weather(city))

                st.markdown("**✓ Checklist Saved**")
                items = Database.load_items(trip_id)
                if items:
                    for item_text, checked in items:
                        icon = "☑" if checked else "☐"
                        text_format = f"~~{item_text}~~" if checked else item_text
                        st.markdown(f"{icon} {text_format}")
                else:
                    st.caption("No items saved for this journey.")
