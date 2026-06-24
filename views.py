# views.py
import streamlit as st
from database import Database

def create_auth_page():
    _, center_col, _ = st.columns([1, 2, 1])
    
    with center_col:
        st.markdown("<h1 style='text-align: center; font-weight: 300; letter-spacing: -1px; color: #D4AF37;'>🧭 Seyahatify</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #888888; font-size: 14px;'>Your minimalist travel companion</p>", unsafe_allow_html=True)
        st.space = st.empty() 
        
        with st.container(border=True):
            tab1, tab2 = st.tabs(["Sign In", "Register"])
            
            with tab1:
                login_user = st.text_input("Username", key="login_user", placeholder="e.g. wanderlust")
                login_pass = st.text_input("Password", type="password", key="login_pass", placeholder="••••••••")
                st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
                
                if st.button("Access Dashboard", type="primary", use_container_width=True):
                    user_id = Database.login(login_user, login_pass)
                    if user_id:
                        st.session_state.logged_in_user_id = user_id
                        st.session_state.page = "main"
                        st.rerun()
                    else:
                        st.error("Incorrect username or password.")
            
            with tab2:
                reg_user = st.text_input("Choose Username", key="reg_user", placeholder="e.g. traveler101")
                reg_pass = st.text_input("Choose Password", type="password", key="reg_pass", placeholder="••••••••")
                st.markdown("<div style='padding-top: 10px;'></div>", unsafe_allow_html=True)
                
                if st.button("Create Account", use_container_width=True):
                    if not reg_user or not reg_pass:
                        st.warning("Fields cannot be left blank.")
                    elif Database.register(reg_user, reg_pass):
                        st.success("Account registered! You can now sign in.")
                    else:
                        st.error("This username is already taken.")

def create_main_page():
    # --- MINIMAL SIDEBAR (Checklist Layout) ---
    with st.sidebar:
        st.markdown("<h3 style='font-weight: 400; letter-spacing: -0.5px;'>Trip Checklist</h3>", unsafe_allow_html=True)
        
        new_todo = st.text_input("Add task item", key="todo_input", placeholder="Pack passport...")
        if st.button("Add to List", use_container_width=True):
            if new_todo.strip():
                st.session_state.checklist.append({"text": new_todo.strip(), "checked": False})
                st.rerun()
        
        st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)
        
        updated_checklist = []
        for idx, item in enumerate(st.session_state.checklist):
            is_checked = st.checkbox(item["text"], value=item["checked"], key=f"todo_check_{idx}")
            updated_checklist.append({"text": item["text"], "checked": is_checked})
        st.session_state.checklist = updated_checklist

        if st.session_state.checklist:
            if st.button("Clear Checked Items", use_container_width=True):
                st.session_state.checklist = [i for i in st.session_state.checklist if not i["checked"]]
                st.rerun()

        st.divider()
        
        if st.button("💾 Save Journey Layout", type="primary", use_container_width=True):
            city = st.session_state.get("city_search_val", "").strip()
            if not city:
                st.warning("Please specify a target destination city first.")
            elif not st.session_state.checklist:
                st.warning("Please add at least one item to your list.")
            else:
                Database.save_trip(st.session_state.logged_in_user_id, city, st.session_state.checklist)
                st.success(f"Trip layout to {city.title()} saved.")

        if st.button("📋 View Archive History", use_container_width=True):
            st.session_state.page = "history"
            st.rerun()

    # --- MAIN ENGINE VIEW ---
    # FIXED: Changed font-weight to 700 to bold the heading section
    st.markdown("<h2 style='font-weight: 700; letter-spacing: -1px;'>Where are we heading?</h2>", unsafe_allow_html=True)
    
    search_col, button_col = st.columns([4, 1])
    with search_col:
        city_entry = st.text_input("Search City", value=st.session_state.get("city_search_val", ""), label_visibility="collapsed", placeholder="Enter city name (e.g. Paris)")
    with button_col:
        search_clicked = st.button("Explore", type="primary", use_container_width=True)
        
    if search_clicked:
        if city_entry.strip():
            st.session_state.city_search_val = city_entry.strip()
            st.session_state.weather_cache = Database.fetch_weather(city_entry.strip())
            st.session_state.tripadvisor_cache = Database.fetch_tripadvisor(city_entry.strip())
            st.rerun()
        else:
            st.warning("Please input a valid target location name.")

    st.markdown("<div style='margin: 20px 0;'></div>", unsafe_allow_html=True)
    
    left_panel, right_panel = st.columns([2, 3])

    # Left Panel: Weather Summary Bento Box
    with left_panel:
        if "weather_cache" in st.session_state:
            if "⚠" in st.session_state.weather_cache:
                weather_content = f"<p style='color:#ff4b4b;margin:0;'>{st.session_state.weather_cache}</p>"
            else:
                lines = st.session_state.weather_cache.split('  |  ')
                lines_html = "".join([f"<p style='margin:8px 0;font-size:15px;'>{line.strip()}</p>" for line in lines])
                weather_content = f"<h3 style='margin:0 0 10px 0;font-weight:600;letter-spacing:-0.5px;'>{st.session_state.city_search_val.title()}</h3>{lines_html}"
        else:
            weather_content = "<p style='color:#8e8e93;font-size:14px;margin:0;'>Awaiting destination choice...</p>"
        
        weather_bento_html = f"<div class='ios-bento'><p class='bento-tag'>🌤 Weather Report</p>{weather_content}</div>".replace("\n", "").replace("\r", "")
        st.markdown(weather_bento_html, unsafe_allow_html=True)

    # Right Panel: TripAdvisor Travel Advice Bento Box (iOS UI Styling)
    with right_panel:
        if "tripadvisor_cache" in st.session_state and st.session_state.tripadvisor_cache:
            advice_html = ""
            for idx, item in enumerate(st.session_state.tripadvisor_cache[:5], 1):
                raw_title = item.get('title', item.get('name', 'Premium Location'))
                title = raw_title.replace("'", "&#39;").replace('"', '&quot;').strip()
                
                url = item.get('link', '#')
                rating = item.get('rating', 'N/A')
                reviews = item.get('reviews', 0)
                
                description = item.get('description', item.get('snippet', ''))
                description = description.replace("'", "&#39;").replace('"', '&quot;').strip()
                
                # FIXED: Removed color:#cccccc, increased font size, added text-align: justify, and applied 0.85 opacity for high-contrast readability
                desc_snippet = f"<p style='font-size:14px; text-align: justify; margin:6px 0 0 0; line-height:1.5; opacity: 0.85;'>{description}</p>" if description else ""
                
                advice_html += (
                    f"<div style='margin-bottom:14px; padding-bottom:14px; border-bottom:1px solid rgba(142,142,147,0.15);'>"
                    f"<a href='{url}' style='text-decoration:none; color:inherit;' target='_blank'>"
                    f"<h5 style='font-weight:600; margin:0 0 3px 0; font-size:16px; color:#007AFF;'>{title}</h5>"
                    f"</a>"
                    f"<p style='font-size:11px; color:#8e8e93; margin:0;'>⭐ {rating} ({reviews} reviews) • Recommendation #{idx}</p>"
                    f"{desc_snippet}"
                    f"</div>"
                )
            advice_content = f"<div style='margin-top:6px;'>{advice_html}</div>"
        elif "tripadvisor_cache" in st.session_state:
            advice_content = "<p style='color:#8e8e93;font-size:14px;margin:0;'>No TripAdvisor travel entries found for this destination.</p>"
        else:
            advice_content = "<p style='color:#8e8e93;font-size:14px;margin:0;'>Awaiting destination choice...</p>"

        tripadvisor_bento_html = f"<div class='ios-bento'><p class='bento-tag'>🧳 TripAdvisor Travel Advice</p>{advice_content}</div>".replace("\n", "").replace("\r", "")
        st.markdown(tripadvisor_bento_html, unsafe_allow_html=True)

def create_history_page():
    top_col1, top_col2 = st.columns([4, 1])
    with top_col1:
        st.markdown("<h2 style='font-weight: 300; letter-spacing: -1px;'>Saved Journeys Archive</h2>", unsafe_allow_html=True)
    with top_col2:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = "main"
            st.rerun()

    sort_option = st.selectbox("Order Sequence Filter", ["Newest First", "Oldest First", "Alphabetical (A → Z)"], label_visibility="collapsed")
    sort_mapping = {"Newest First": "newest", "Oldest First": "oldest", "Alphabetical (A → Z)": "atoz"}
    
    sorted_trips = Database.load_trips(st.session_state.logged_in_user_id, sort_mapping[sort_option])
    st.markdown("<div style='margin: 15px 0;'></div>", unsafe_allow_html=True)

    if not sorted_trips:
        st.info("No logs present inside this profile catalog yet.")
        return

    cols = st.columns(2)
    for idx, (trip_id, city) in enumerate(sorted_trips):
        with cols[idx % 2]:
            with st.container(border=True):
                card_head_left, card_head_right = st.columns([5, 1])
                card_head_left.markdown(f"<h4 style='font-weight: 400; margin: 0;'>{city.title()}</h4>", unsafe_allow_html=True)
                
                if card_head_right.button("✕", key=f"del_{trip_id}", help="Delete log"):
                    Database.delete_trip(trip_id)
                    st.rerun()
                
                st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
                st.markdown("<p style='font-size: 11px; text-transform: uppercase; color: #888888; margin-bottom: 2px;'>Weather Capture</p>", unsafe_allow_html=True)
                
                weather_str = Database.fetch_weather(city).replace('\n', '  |  ')
                st.markdown(f"<p style='font-size: 13px; color: #cccccc;'>{weather_str}</p>", unsafe_allow_html=True)
                st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
                
                items = Database.load_items(trip_id)
                pending_items = [item_text for item_text, checked in items if not checked]
                completed_items = [item_text for item_text, checked in items if checked]
                
                if pending_items:
                    st.markdown("<p style='font-size: 11px; text-transform: uppercase; color: #ffbc00; margin-bottom: 4px;'>⏳ Remaining Tasks</p>", unsafe_allow_html=True)
                    for item_text in pending_items:
                        st.markdown(f"<p style='font-size: 13px; margin: 2px 0; color: #ffffff;'>◦ {item_text}</p>", unsafe_allow_html=True)
                
                if completed_items:
                    if pending_items:
                        st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size: 11px; text-transform: uppercase; color: #00fa9a; margin-bottom: 4px;'>✅ Completed Tasks</p>", unsafe_allow_html=True)
                    for item_text in completed_items:
                        st.markdown(f"<p style='font-size: 13px; margin: 2px 0; text-decoration: line-through; color: #666666;'>• {item_text}</p>", unsafe_allow_html=True)
                
                if not items:
                    st.caption("Zero tasks assigned to this itinerary registry index.")
                
                st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)
                
                copy_text = f"📌 SEYAHATIFY TRAVEL PACK: {city.title()}\n"
                copy_text += f"🌤️ Weather Profile: {weather_str}\n\n"
                copy_text += "⏳ REMAINING TO-DO ITEMS:\n"
                if pending_items:
                    for item in pending_items:
                        copy_text += f"  - [ ] {item}\n"
                else:
                    copy_text += "  (None)\n"
                
                copy_text += "\n✅ COMPLETED ITEMS:\n"
                if completed_items:
                    for item in completed_items:
                        copy_text += f"  - [x] {item}\n"
                else:
                    copy_text += "  (None)\n"
                
                st.code(copy_text, language=None)
